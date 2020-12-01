/*
 * Copyright 2020 The TensorFlow Runtime Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

//===- request_handler_impl.h -----------------------------------*- C++ -*-===//
//
// This file declares public function to create RequestHandler implementation.
//
//===----------------------------------------------------------------------===//

#ifndef TFRT_DISTRIBUTED_RUNTIME_REQUEST_HANDLER_IMPL_H_
#define TFRT_DISTRIBUTED_RUNTIME_REQUEST_HANDLER_IMPL_H_

#include "tfrt/distributed_runtime/request_handler.h"

namespace tfrt {

class ServerContext;

std::unique_ptr<RequestHandlerInterface> NewRequestHandler(
    ServerContext* server_context);

}  // namespace tfrt

#endif  // TFRT_DISTRIBUTED_RUNTIME_REQUEST_HANDLER_IMPL_H_
