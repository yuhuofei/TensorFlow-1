// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/protobuf/saved_model.proto

package org.tensorflow.proto.framework;

public final class SavedModelProtos {
  private SavedModelProtos() {}
  public static void registerAllExtensions(
      com.google.protobuf.ExtensionRegistryLite registry) {
  }

  public static void registerAllExtensions(
      com.google.protobuf.ExtensionRegistry registry) {
    registerAllExtensions(
        (com.google.protobuf.ExtensionRegistryLite) registry);
  }
  static final com.google.protobuf.Descriptors.Descriptor
    internal_static_tensorflow_SavedModel_descriptor;
  static final 
    com.google.protobuf.GeneratedMessageV3.FieldAccessorTable
      internal_static_tensorflow_SavedModel_fieldAccessorTable;

  public static com.google.protobuf.Descriptors.FileDescriptor
      getDescriptor() {
    return descriptor;
  }
  private static  com.google.protobuf.Descriptors.FileDescriptor
      descriptor;
  static {
    java.lang.String[] descriptorData = {
      "\n*tensorflow/core/protobuf/saved_model.p" +
      "roto\022\ntensorflow\032)tensorflow/core/protob" +
      "uf/meta_graph.proto\"_\n\nSavedModel\022\"\n\032sav" +
      "ed_model_schema_version\030\001 \001(\003\022-\n\013meta_gr" +
      "aphs\030\002 \003(\0132\030.tensorflow.MetaGraphDefB\201\001\n" +
      "\036org.tensorflow.proto.frameworkB\020SavedMo" +
      "delProtosP\001ZHgithub.com/tensorflow/tenso" +
      "rflow/tensorflow/go/core/core_protos_go_" +
      "proto\370\001\001b\006proto3"
    };
    descriptor = com.google.protobuf.Descriptors.FileDescriptor
      .internalBuildGeneratedFileFrom(descriptorData,
        new com.google.protobuf.Descriptors.FileDescriptor[] {
          org.tensorflow.proto.framework.MetaGraphProtos.getDescriptor(),
        });
    internal_static_tensorflow_SavedModel_descriptor =
      getDescriptor().getMessageTypes().get(0);
    internal_static_tensorflow_SavedModel_fieldAccessorTable = new
      com.google.protobuf.GeneratedMessageV3.FieldAccessorTable(
        internal_static_tensorflow_SavedModel_descriptor,
        new java.lang.String[] { "SavedModelSchemaVersion", "MetaGraphs", });
    org.tensorflow.proto.framework.MetaGraphProtos.getDescriptor();
  }

  // @@protoc_insertion_point(outer_class_scope)
}
