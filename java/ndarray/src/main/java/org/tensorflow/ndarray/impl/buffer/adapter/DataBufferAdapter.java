/*
 *  Copyright 2019 The TensorFlow Authors. All Rights Reserved.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *  =======================================================================
 */

package org.tensorflow.ndarray.impl.buffer.adapter;

import org.tensorflow.ndarray.buffer.DataBuffer;
import org.tensorflow.ndarray.buffer.layout.DataLayout;

@SuppressWarnings("unchecked")
class DataBufferAdapter<S extends DataBuffer<?>, T> extends AbstractDataBufferAdapter<S, T, DataBuffer<T>> {

  @Override
  @SuppressWarnings("unchecked")
  public DataBuffer<T> offset(long index) {
    return new DataBufferAdapter<>((S)buffer().offset(index * layout().scale()), layout());
  }

  @Override
  @SuppressWarnings("unchecked")
  public DataBuffer<T> narrow(long size) {
    return new DataBufferAdapter<>((S)buffer().narrow(size * layout().scale()), layout());
  }

  @Override
  @SuppressWarnings("unchecked")
  public DataBuffer<T> slice(long index, long size) {
    return new DataBufferAdapter<>((S)buffer().slice(index * layout().scale(), size * layout().scale()), layout());
  }

  DataBufferAdapter(S buffer, DataLayout<S, T> layout) {
    super(buffer, layout);
  }
}
