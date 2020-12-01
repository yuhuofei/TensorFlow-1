# coding=utf-8
# Copyright 2020 TF.Text Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# encoding=utf-8
# Lint as: python3
"""Tests for regex_split and regex_split_with_offsets ops."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import parameterized

from tensorflow.python.framework import constant_op
from tensorflow.python.framework import test_util
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import string_ops
from tensorflow.python.ops.ragged import ragged_factory_ops
from tensorflow.python.ops.ragged import ragged_tensor
from tensorflow.python.platform import test
from tensorflow_text.python.ops import regex_split_ops


def _utf8(char):
  return char.encode("utf-8")


# TODO(thuang513): It appears there isn't a Ragged version of substr; consider
#               checking this into core TF.
def _ragged_substr(text_input, begin, end):
  text_input_flat = None
  if ragged_tensor.is_ragged(text_input):
    text_input_flat = text_input.flat_values
  else:
    text_input_flat = array_ops.reshape(text_input, [-1])
  broadcasted_text = array_ops.gather_v2(text_input_flat,
                                         begin.nested_value_rowids()[-1])
  size = math_ops.sub(end.flat_values, begin.flat_values)
  new_tokens = string_ops.substr_v2(broadcasted_text, begin.flat_values, size)
  return begin.with_flat_values(new_tokens)


@test_util.run_all_in_graph_and_eager_modes
class RegexSplitOpsTest(parameterized.TestCase, test.TestCase):

  @parameterized.parameters([
      dict(
          descr="Test doc string examples",
          text_input=[r"hello there"],
          delim_regex_pattern=r"\s",
          keep_delim_regex_pattern=r"\s",
          expected=[[b"hello", b" ", b"there"]],
      ),
      dict(
          descr="Test simple whitespace",
          text_input=[r"hello there"],
          delim_regex_pattern=r"\s",
          expected=[[b"hello", b"there"]],
      ),
      dict(
          descr="Two delimiters in a row",
          text_input=[r"hello  there"],
          delim_regex_pattern=r"\s",
          expected=[[b"hello", b"there"]],
      ),
      dict(
          descr="Test Hiragana",
          text_input=[_utf8(u"では４日")],
          delim_regex_pattern=r"\p{Hiragana}",
          keep_delim_regex_pattern=r"\p{Hiragana}",
          expected=[[_utf8(u"で"), _utf8(u"は"),
                     _utf8(u"４日")]],
      ),
      dict(
          descr="Test symbols and punctuation",
          text_input=[r"hello! (:$) there"],
          delim_regex_pattern=r"[\p{S}|\p{P}]+|\s",
          keep_delim_regex_pattern=r"[\p{S}|\p{P}]+",
          expected=[[b"hello", b"!", b"(:$)", b"there"]],
      ),
      dict(
          descr="Test numbers",
          text_input=[r"hello12345there"],
          delim_regex_pattern=r"\p{N}+",
          keep_delim_regex_pattern=r"\p{N}+",
          expected=[[b"hello", b"12345", b"there"]],
      ),
      dict(
          descr="Test numbers and symbols",
          text_input=[r"show me some $100 bills yo!"],
          delim_regex_pattern=r"\s|\p{S}",
          keep_delim_regex_pattern=r"\p{S}",
          expected=[[b"show", b"me", b"some", b"$", b"100", b"bills", b"yo!"]],
      ),
      dict(
          descr="Test input RaggedTensor with ragged ranks; "
          "shape = [2, (1, 2)]",
          text_input=[
              [b"show me some $100 bills yo!",
               _utf8(u"では４日")],
              [b"hello there"],
          ],
          delim_regex_pattern=r"\s|\p{S}|\p{Hiragana}",
          keep_delim_regex_pattern=r"\p{S}|\p{Hiragana}",
          expected=[[[b"show", b"me", b"some", b"$", b"100", b"bills", b"yo!"],
                     [_utf8(u"で"), _utf8(u"は"),
                      _utf8(u"４日")]], [[b"hello", b"there"]]],
      ),
      # Test inputs that are Tensors.
      dict(
          descr="Test input Tensor with shape = [2], rank = 1",
          text_input=[
              r"show me some $100 bills yo!",
              r"hello there",
          ],
          delim_regex_pattern=r"\s|\p{S}",
          keep_delim_regex_pattern=r"\p{S}",
          expected=[[b"show", b"me", b"some", b"$", b"100", b"bills", b"yo!"],
                    [b"hello", b"there"]],
          input_is_dense=True,
      ),
      dict(
          descr="Test input Tensor with shape = [2, 1], rank = 2",
          text_input=[
              [r"show me some $100 bills yo!"],
              [r"hello there"],
          ],
          delim_regex_pattern=r"\s|\p{S}",
          keep_delim_regex_pattern=r"\p{S}",
          expected=[[[b"show", b"me", b"some", b"$", b"100", b"bills", b"yo!"]],
                    [[b"hello", b"there"]]],
          input_is_dense=True,
      ),
      dict(
          descr="Test input Tensor with multiple ranks; shape = [2, 2]",
          input_is_dense=True,
          text_input=[
              [b"show me some $100 bills yo!",
               _utf8(u"では４日")],
              [b"hello there", b"woot woot"],
          ],
          delim_regex_pattern=r"\s|\p{S}|\p{Hiragana}",
          keep_delim_regex_pattern=r"\p{S}|\p{Hiragana}",
          expected=[[[b"show", b"me", b"some", b"$", b"100", b"bills", b"yo!"],
                     [_utf8(u"で"), _utf8(u"は"),
                      _utf8(u"４日")]], [[b"hello", b"there"], [b"woot",
                                                              b"woot"]]],
      ),
      dict(
          descr="Test input Tensor with multiple; shape = [2, 2, 1]",
          input_is_dense=True,
          text_input=[
              [[b"show me some $100 bills yo!"], [_utf8(u"では４日")]],
              [[b"hello there"], [b"woot woot"]],
          ],
          delim_regex_pattern=r"\s|\p{S}|\p{Hiragana}",
          keep_delim_regex_pattern=r"\p{S}|\p{Hiragana}",
          # expected shape = [2, 2, 1, ]
          expected=[[[[b"show", b"me", b"some", b"$", b"100", b"bills",
                       b"yo!"]], [[_utf8(u"で"),
                                   _utf8(u"は"),
                                   _utf8(u"４日")]]],
                    [[[b"hello", b"there"]], [[b"woot", b"woot"]]]],
      ),
  ])
  def testRegexSplitOp(self,
                       text_input,
                       delim_regex_pattern,
                       expected,
                       keep_delim_regex_pattern=r"",
                       descr="",
                       input_is_dense=False):
    if input_is_dense:
      text_input = constant_op.constant(text_input)
    else:
      text_input = ragged_factory_ops.constant(text_input)

    actual_tokens, start, end = regex_split_ops.regex_split_with_offsets(
        input=text_input,
        delim_regex_pattern=delim_regex_pattern,
        keep_delim_regex_pattern=keep_delim_regex_pattern,
    )
    self.assertAllEqual(actual_tokens, expected)

    # Use the offsets to extract substrings and verify that the substrings match
    # up with the expected tokens
    extracted_tokens = _ragged_substr(text_input, start, end)
    self.assertAllEqual(extracted_tokens, expected)


if __name__ == "__main__":
  test.main()
