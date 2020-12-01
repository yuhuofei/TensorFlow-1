// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/profiler/protobuf/xplane.proto

package org.tensorflow.proto.profiler;

public interface XPlaneOrBuilder extends
    // @@protoc_insertion_point(interface_extends:tensorflow.profiler.XPlane)
    com.google.protobuf.MessageOrBuilder {

  /**
   * <code>int64 id = 1;</code>
   */
  long getId();

  /**
   * <pre>
   * Name of this line.
   * </pre>
   *
   * <code>string name = 2;</code>
   */
  java.lang.String getName();
  /**
   * <pre>
   * Name of this line.
   * </pre>
   *
   * <code>string name = 2;</code>
   */
  com.google.protobuf.ByteString
      getNameBytes();

  /**
   * <pre>
   * Parallel timelines grouped in this plane. XLines with the same id
   * are effectively the same timeline.
   * </pre>
   *
   * <code>repeated .tensorflow.profiler.XLine lines = 3;</code>
   */
  java.util.List<org.tensorflow.proto.profiler.XLine> 
      getLinesList();
  /**
   * <pre>
   * Parallel timelines grouped in this plane. XLines with the same id
   * are effectively the same timeline.
   * </pre>
   *
   * <code>repeated .tensorflow.profiler.XLine lines = 3;</code>
   */
  org.tensorflow.proto.profiler.XLine getLines(int index);
  /**
   * <pre>
   * Parallel timelines grouped in this plane. XLines with the same id
   * are effectively the same timeline.
   * </pre>
   *
   * <code>repeated .tensorflow.profiler.XLine lines = 3;</code>
   */
  int getLinesCount();
  /**
   * <pre>
   * Parallel timelines grouped in this plane. XLines with the same id
   * are effectively the same timeline.
   * </pre>
   *
   * <code>repeated .tensorflow.profiler.XLine lines = 3;</code>
   */
  java.util.List<? extends org.tensorflow.proto.profiler.XLineOrBuilder> 
      getLinesOrBuilderList();
  /**
   * <pre>
   * Parallel timelines grouped in this plane. XLines with the same id
   * are effectively the same timeline.
   * </pre>
   *
   * <code>repeated .tensorflow.profiler.XLine lines = 3;</code>
   */
  org.tensorflow.proto.profiler.XLineOrBuilder getLinesOrBuilder(
      int index);

  /**
   * <pre>
   * XEventMetadata map, each entry uses the XEventMetadata.id as key. This map
   * should be used for events that share the same ID over the whole XPlane.
   * </pre>
   *
   * <code>map&lt;int64, .tensorflow.profiler.XEventMetadata&gt; event_metadata = 4;</code>
   */
  int getEventMetadataCount();
  /**
   * <pre>
   * XEventMetadata map, each entry uses the XEventMetadata.id as key. This map
   * should be used for events that share the same ID over the whole XPlane.
   * </pre>
   *
   * <code>map&lt;int64, .tensorflow.profiler.XEventMetadata&gt; event_metadata = 4;</code>
   */
  boolean containsEventMetadata(
      long key);
  /**
   * Use {@link #getEventMetadataMap()} instead.
   */
  @java.lang.Deprecated
  java.util.Map<java.lang.Long, org.tensorflow.proto.profiler.XEventMetadata>
  getEventMetadata();
  /**
   * <pre>
   * XEventMetadata map, each entry uses the XEventMetadata.id as key. This map
   * should be used for events that share the same ID over the whole XPlane.
   * </pre>
   *
   * <code>map&lt;int64, .tensorflow.profiler.XEventMetadata&gt; event_metadata = 4;</code>
   */
  java.util.Map<java.lang.Long, org.tensorflow.proto.profiler.XEventMetadata>
  getEventMetadataMap();
  /**
   * <pre>
   * XEventMetadata map, each entry uses the XEventMetadata.id as key. This map
   * should be used for events that share the same ID over the whole XPlane.
   * </pre>
   *
   * <code>map&lt;int64, .tensorflow.profiler.XEventMetadata&gt; event_metadata = 4;</code>
   */

  org.tensorflow.proto.profiler.XEventMetadata getEventMetadataOrDefault(
      long key,
      org.tensorflow.proto.profiler.XEventMetadata defaultValue);
  /**
   * <pre>
   * XEventMetadata map, each entry uses the XEventMetadata.id as key. This map
   * should be used for events that share the same ID over the whole XPlane.
   * </pre>
   *
   * <code>map&lt;int64, .tensorflow.profiler.XEventMetadata&gt; event_metadata = 4;</code>
   */

  org.tensorflow.proto.profiler.XEventMetadata getEventMetadataOrThrow(
      long key);

  /**
   * <pre>
   * XStatMetadata map, each entry uses the XStatMetadata.id as key. This map
   * should be used for stats that share the same ID over the whole XPlane.
   * </pre>
   *
   * <code>map&lt;int64, .tensorflow.profiler.XStatMetadata&gt; stat_metadata = 5;</code>
   */
  int getStatMetadataCount();
  /**
   * <pre>
   * XStatMetadata map, each entry uses the XStatMetadata.id as key. This map
   * should be used for stats that share the same ID over the whole XPlane.
   * </pre>
   *
   * <code>map&lt;int64, .tensorflow.profiler.XStatMetadata&gt; stat_metadata = 5;</code>
   */
  boolean containsStatMetadata(
      long key);
  /**
   * Use {@link #getStatMetadataMap()} instead.
   */
  @java.lang.Deprecated
  java.util.Map<java.lang.Long, org.tensorflow.proto.profiler.XStatMetadata>
  getStatMetadata();
  /**
   * <pre>
   * XStatMetadata map, each entry uses the XStatMetadata.id as key. This map
   * should be used for stats that share the same ID over the whole XPlane.
   * </pre>
   *
   * <code>map&lt;int64, .tensorflow.profiler.XStatMetadata&gt; stat_metadata = 5;</code>
   */
  java.util.Map<java.lang.Long, org.tensorflow.proto.profiler.XStatMetadata>
  getStatMetadataMap();
  /**
   * <pre>
   * XStatMetadata map, each entry uses the XStatMetadata.id as key. This map
   * should be used for stats that share the same ID over the whole XPlane.
   * </pre>
   *
   * <code>map&lt;int64, .tensorflow.profiler.XStatMetadata&gt; stat_metadata = 5;</code>
   */

  org.tensorflow.proto.profiler.XStatMetadata getStatMetadataOrDefault(
      long key,
      org.tensorflow.proto.profiler.XStatMetadata defaultValue);
  /**
   * <pre>
   * XStatMetadata map, each entry uses the XStatMetadata.id as key. This map
   * should be used for stats that share the same ID over the whole XPlane.
   * </pre>
   *
   * <code>map&lt;int64, .tensorflow.profiler.XStatMetadata&gt; stat_metadata = 5;</code>
   */

  org.tensorflow.proto.profiler.XStatMetadata getStatMetadataOrThrow(
      long key);

  /**
   * <pre>
   * XStats associated with this plane, e.g. device capabilities.
   * </pre>
   *
   * <code>repeated .tensorflow.profiler.XStat stats = 6;</code>
   */
  java.util.List<org.tensorflow.proto.profiler.XStat> 
      getStatsList();
  /**
   * <pre>
   * XStats associated with this plane, e.g. device capabilities.
   * </pre>
   *
   * <code>repeated .tensorflow.profiler.XStat stats = 6;</code>
   */
  org.tensorflow.proto.profiler.XStat getStats(int index);
  /**
   * <pre>
   * XStats associated with this plane, e.g. device capabilities.
   * </pre>
   *
   * <code>repeated .tensorflow.profiler.XStat stats = 6;</code>
   */
  int getStatsCount();
  /**
   * <pre>
   * XStats associated with this plane, e.g. device capabilities.
   * </pre>
   *
   * <code>repeated .tensorflow.profiler.XStat stats = 6;</code>
   */
  java.util.List<? extends org.tensorflow.proto.profiler.XStatOrBuilder> 
      getStatsOrBuilderList();
  /**
   * <pre>
   * XStats associated with this plane, e.g. device capabilities.
   * </pre>
   *
   * <code>repeated .tensorflow.profiler.XStat stats = 6;</code>
   */
  org.tensorflow.proto.profiler.XStatOrBuilder getStatsOrBuilder(
      int index);
}
