# Copyright 2020 The TensorFlow Probability Authors.
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
# ============================================================================
"""Auto-generate TensorShape replacements."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import importlib
import inspect

# Dependency imports

from absl import app
from absl import flags

FLAGS = flags.FLAGS

COMMENT_OUT = [
    'from tensorflow.core.framework import tensor_shape_pb2',
    'from tensorflow.python import tf2',
    'from tensorflow.python.eager import monitoring',
    'from tensorflow.python.util.tf_export import tf_export',
    'from __future__',
]

PREAMBLE = """
\"\"\"TensorShape, for numpy & jax.\"\"\"
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

class Monitoring(object):
  def __getattr__(self, name):
    return lambda *args, **kwargs: ()
monitoring = Monitoring()
def tf_export(*args, **kwargs):
  return lambda f: f
"""


POSTAMBLE = """
TensorShape._v2_behavior = True
class TensorShapePb2:
  def __init__(self):
    class _dummy:
      pass
    self.TensorShapeProto = _dummy
tensor_shape_pb2 = TensorShapePb2()
"""


def gen_tensor_shape():
  """Rewrite for numpy the code loaded from the given linalg module."""
  module = importlib.import_module(
      'tensorflow.python.framework.tensor_shape')
  code = inspect.getsource(module)
  for k in COMMENT_OUT:
    code = code.replace(k, '# {}'.format(k))
  code = code.replace('tf2.enabled()', 'True  # tf2.enabled()')

  print('# Copyright 2020 The TensorFlow Probability Authors. '
        'All Rights Reserved.')
  print('# ' + '@' * 78)
  print('# THIS FILE IS AUTO-GENERATED BY `gen_tensor_shape.py`.')
  print('# DO NOT MODIFY DIRECTLY.')
  print('# ' + '@' * 78)
  print('# pylint: disable=g-statement-before-imports')
  print('# pylint: disable=protected-access')
  print('# pylint: disable=invalid-name')
  print('# pylint: disable=pointless-string-statement')
  print('# pylint: disable=unused-argument')
  print('# pylint: disable=g-wrong-blank-lines')
  print(PREAMBLE)
  print(code)
  print(POSTAMBLE)


def main(_):
  gen_tensor_shape()


if __name__ == '__main__':
  app.run(main)
