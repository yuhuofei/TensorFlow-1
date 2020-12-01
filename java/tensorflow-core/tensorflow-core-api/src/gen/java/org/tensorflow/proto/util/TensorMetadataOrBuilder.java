// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/protobuf/data/experimental/snapshot.proto

package org.tensorflow.proto.util;

public interface TensorMetadataOrBuilder extends
    // @@protoc_insertion_point(interface_extends:tensorflow.data.experimental.TensorMetadata)
    com.google.protobuf.MessageOrBuilder {

  /**
   * <code>.tensorflow.TensorShapeProto tensor_shape = 2;</code>
   */
  boolean hasTensorShape();
  /**
   * <code>.tensorflow.TensorShapeProto tensor_shape = 2;</code>
   */
  org.tensorflow.proto.framework.TensorShapeProto getTensorShape();
  /**
   * <code>.tensorflow.TensorShapeProto tensor_shape = 2;</code>
   */
  org.tensorflow.proto.framework.TensorShapeProtoOrBuilder getTensorShapeOrBuilder();

  /**
   * <pre>
   * Number of uncompressed bytes used to store the tensor representation.
   * </pre>
   *
   * <code>int64 tensor_size_bytes = 3;</code>
   */
  long getTensorSizeBytes();
}
