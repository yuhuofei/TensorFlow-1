#!/usr/bin/env bash
# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================

set -e
set -o pipefail

if [ "$#" -eq 1 ]; then
  container=$1
  echo pull localstack/localstack:0.8.10
  docker pull localstack/localstack:0.8.10
  echo pull localstack/localstack:0.8.10 successfully
  docker run -d --rm -p 4568:4568 --name=$container localstack/localstack:0.8.10
  echo Container $container started successfully

  exit 0
fi

if [[ $(uname) == "Darwin" ]]; then
    pip install -q --user localstack
    $HOME/Library/Python/2.7/bin/localstack start --host &
else
    sudo apt-get install -y -qq python-dev libsasl2-dev gcc
    python -m pip install --user -U pip
    python -m pip install --user -U setuptools wheel
    python -m pip install --user localstack
    $HOME/.local/bin/localstack start --host &
fi
exit 0
