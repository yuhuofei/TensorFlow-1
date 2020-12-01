// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/profiler/protobuf/xplane.proto

package org.tensorflow.proto.profiler;

public interface XEventMetadataOrBuilder extends
    // @@protoc_insertion_point(interface_extends:tensorflow.profiler.XEventMetadata)
    com.google.protobuf.MessageOrBuilder {

  /**
   * <pre>
   * XPlane.event_metadata map key.
   * </pre>
   *
   * <code>int64 id = 1;</code>
   */
  long getId();

  /**
   * <pre>
   * Name of the event.
   * </pre>
   *
   * <code>string name = 2;</code>
   */
  java.lang.String getName();
  /**
   * <pre>
   * Name of the event.
   * </pre>
   *
   * <code>string name = 2;</code>
   */
  com.google.protobuf.ByteString
      getNameBytes();

  /**
   * <pre>
   * Name of the event shown in trace viewer.
   * </pre>
   *
   * <code>string display_name = 4;</code>
   */
  java.lang.String getDisplayName();
  /**
   * <pre>
   * Name of the event shown in trace viewer.
   * </pre>
   *
   * <code>string display_name = 4;</code>
   */
  com.google.protobuf.ByteString
      getDisplayNameBytes();

  /**
   * <pre>
   * Additional metadata in serialized format.
   * </pre>
   *
   * <code>bytes metadata = 3;</code>
   */
  com.google.protobuf.ByteString getMetadata();
}
