# Copyright 2018, The TensorFlow Federated Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Bodies of intrinsics to be added as replacements by the compiler pipleine."""

import collections
from typing import Callable, Dict

import tensorflow as tf

from tensorflow_federated.python.common_libs import py_typecheck
from tensorflow_federated.python.core.api import computation_types
from tensorflow_federated.python.core.impl import intrinsic_factory
from tensorflow_federated.python.core.impl import value_impl
from tensorflow_federated.python.core.impl.compiler import building_block_factory
from tensorflow_federated.python.core.impl.compiler import building_blocks
from tensorflow_federated.python.core.impl.compiler import intrinsic_defs
from tensorflow_federated.python.core.impl.context_stack import context_stack_base
from tensorflow_federated.python.core.impl.types import type_analysis


def _only_tuple_or_tensor(x: computation_types.Type) -> bool:
  return type_analysis.contains_only(x,
                                     lambda t: t.is_struct() or t.is_tensor())


def _federated_same_placement(x: computation_types.Type,
                              y: computation_types.Type) -> bool:
  return x.is_federated() and y.is_federated() and x.placement == y.placement


def _pack_binary_operator_args(x, y, intrinsics, context_stack):
  """Packs arguments to binary operator into a single arg."""
  x_type = x.type_signature
  y_type = y.type_signature
  if _only_tuple_or_tensor(x_type) and _only_tuple_or_tensor(y_type):
    needs_zip = False
  else:
    if not type_analysis.contains(x_type, lambda t: t.is_federated()):
      raise TypeError
    needs_zip = True

  arg = value_impl.ValueImpl(
      building_blocks.Struct(
          [value_impl.ValueImpl.get_comp(x),
           value_impl.ValueImpl.get_comp(y)]), context_stack)
  if needs_zip:
    arg = intrinsics.federated_zip(arg)
  return arg


def _apply_generic_op(op, x, y, intrinsics, context_stack):
  arg = _pack_binary_operator_args(x, y, intrinsics, context_stack)
  arg_comp = value_impl.ValueImpl.get_comp(arg)
  result = building_block_factory.apply_binary_operator_with_upcast(
      arg_comp, op)
  return value_impl.ValueImpl(result, context_stack)


def get_intrinsic_bodies(
    context_stack
) -> Dict[str, Callable[[value_impl.ValueImpl], value_impl.ValueImpl]]:
  """Returns map from intrinsic to reducing function.

  The returned dictionary is a `collections.OrderedDict` which maps intrinsic
  URIs to functions from intrinsic argument values to a version of the intrinsic
  call which has been reduced to a smaller, more fundamental set of intrinsics.

  Bodies generated by later dictionary entries will not contain references
  to intrinsics whose entries appear earlier in the dictionary. This property
  is useful for simple reduction of an entire computation by iterating through
  the map of intrinsics, substituting calls to each.

  Args:
    context_stack: The context stack to use.
  """
  py_typecheck.check_type(context_stack, context_stack_base.ContextStack)
  intrinsics = intrinsic_factory.IntrinsicFactory(context_stack)

  # TODO(b/122728050): Implement reductions that follow roughly the following
  # breakdown in order to minimize the number of intrinsics that backends need
  # to support and maximize opportunities for merging processing logic to keep
  # the number of communication phases as small as it is practical. Perform
  # these reductions before FEDERATED_SUM (more reductions documented below).
  #
  # - FEDERATED_AGGREGATE(x, zero, accu, merge, report) :=
  #     GENERIC_MAP(
  #       GENERIC_REDUCE(
  #         GENERIC_PARTIAL_REDUCE(x, zero, accu, INTERMEDIATE_AGGREGATORS),
  #         zero, merge, SERVER),
  #       report)
  #
  # - FEDERATED_APPLY(f, x) := GENERIC_APPLY(f, x)
  #
  # - FEDERATED_BROADCAST(x) := GENERIC_BROADCAST(x, CLIENTS)
  #
  # - FEDERATED_COLLECT(x) := GENERIC_COLLECT(x, SERVER)
  #
  # - FEDERATED_MAP(f, x) := GENERIC_MAP(f, x)
  #
  # - FEDERATED_VALUE_AT_CLIENTS(x) := GENERIC_PLACE(x, CLIENTS)
  #
  # - FEDERATED_VALUE_AT_SERVER(x) := GENERIC_PLACE(x, SERVER)

  def federated_weighted_mean(arg):
    w = arg[1]
    multiplied = generic_multiply(arg)
    summed = federated_sum(intrinsics.federated_zip([multiplied, w]))
    return generic_divide(summed)

  def federated_mean(arg):
    one = value_impl.ValueImpl(
        building_block_factory.create_generic_constant(arg.type_signature, 1),
        context_stack)
    arg = value_impl.to_value([arg, one], None, context_stack)
    return federated_weighted_mean(arg)

  def federated_sum(x):
    operand_type = x.type_signature.member
    zero = value_impl.ValueImpl(
        building_block_factory.create_generic_constant(operand_type, 0),
        context_stack)
    plus_op = value_impl.ValueImpl(
        building_block_factory.create_tensorflow_binary_operator_with_upcast(
            computation_types.StructType([operand_type, operand_type]), tf.add),
        context_stack)
    return federated_reduce([x, zero, plus_op])

  def federated_reduce(arg):
    x = arg[0]
    zero = arg[1]
    op = arg[2]
    identity = building_block_factory.create_compiled_identity(
        op.type_signature.result)
    return intrinsics.federated_aggregate(x, zero, op, op, identity)

  def generic_divide(arg):
    """Divides two arguments when possible."""
    return _apply_generic_op(tf.divide, arg[0], arg[1], intrinsics,
                             context_stack)

  def generic_multiply(arg):
    """Multiplies two arguments when possible."""
    return _apply_generic_op(tf.multiply, arg[0], arg[1], intrinsics,
                             context_stack)

  def generic_plus(arg):
    """Adds two arguments when possible."""
    return _apply_generic_op(tf.add, arg[0], arg[1], intrinsics, context_stack)

  # - FEDERATED_ZIP(x, y) := GENERIC_ZIP(x, y)
  #
  # - GENERIC_AVERAGE(x: {T}@p, q: placement) :=
  #     GENERIC_WEIGHTED_AVERAGE(x, GENERIC_ONE, q)
  #
  # - GENERIC_WEIGHTED_AVERAGE(x: {T}@p, w: {U}@p, q: placement) :=
  #     GENERIC_MAP(GENERIC_DIVIDE, GENERIC_SUM(
  #       GENERIC_MAP(GENERIC_MULTIPLY, GENERIC_ZIP(x, w)), p))
  #
  #     Note: The above formula does not account for type casting issues that
  #     arise due to the interplay betwen the types of values and weights and
  #     how they relate to types of products and ratios, and either the formula
  #     or the type signatures may need to be tweaked.
  #
  # - GENERIC_SUM(x: {T}@p, q: placement) :=
  #     GENERIC_REDUCE(x, GENERIC_ZERO, GENERIC_PLUS, q)
  #
  # - GENERIC_PARTIAL_SUM(x: {T}@p, q: placement) :=
  #     GENERIC_PARTIAL_REDUCE(x, GENERIC_ZERO, GENERIC_PLUS, q)
  #
  # - GENERIC_AGGREGATE(
  #     x: {T}@p, zero: U, accu: <U,T>->U, merge: <U,U>=>U, report: U->R,
  #     q: placement) :=
  #     GENERIC_MAP(report, GENERIC_REDUCE(x, zero, accu, q))
  #
  # - GENERIC_REDUCE(x: {T}@p, zero: U, op: <U,T>->U, q: placement) :=
  #     GENERIC_MAP((a -> SEQUENCE_REDUCE(a, zero, op)), GENERIC_COLLECT(x, q))
  #
  # - GENERIC_PARTIAL_REDUCE(x: {T}@p, zero: U, op: <U,T>->U, q: placement) :=
  #     GENERIC_MAP(
  #       (a -> SEQUENCE_REDUCE(a, zero, op)), GENERIC_PARTIAL_COLLECT(x, q))
  #
  # - SEQUENCE_SUM(x: T*) :=
  #     SEQUENCE_REDUCE(x, GENERIC_ZERO, GENERIC_PLUS)
  #
  # After performing the full set of reductions, we should only see instances
  # of the following intrinsics in the result, all of which are currently
  # considered non-reducible, and intrinsics such as GENERIC_PLUS should apply
  # only to non-federated, non-sequence types (with the appropriate calls to
  # GENERIC_MAP or SEQUENCE_MAP injected).
  #
  # - GENERIC_APPLY
  # - GENERIC_BROADCAST
  # - GENERIC_COLLECT
  # - GENERIC_DIVIDE
  # - GENERIC_MAP
  # - GENERIC_MULTIPLY
  # - GENERIC_ONE
  # - GENERIC_ONLY
  # - GENERIC_PARTIAL_COLLECT
  # - GENERIC_PLACE
  # - GENERIC_PLUS
  # - GENERIC_ZERO
  # - GENERIC_ZIP
  # - SEQUENCE_MAP
  # - SEQUENCE_REDUCE

  return collections.OrderedDict([
      (intrinsic_defs.FEDERATED_MEAN.uri, federated_mean),
      (intrinsic_defs.FEDERATED_WEIGHTED_MEAN.uri, federated_weighted_mean),
      (intrinsic_defs.FEDERATED_SUM.uri, federated_sum),
      (intrinsic_defs.GENERIC_DIVIDE.uri, generic_divide),
      (intrinsic_defs.GENERIC_MULTIPLY.uri, generic_multiply),
      (intrinsic_defs.GENERIC_PLUS.uri, generic_plus),
  ])
