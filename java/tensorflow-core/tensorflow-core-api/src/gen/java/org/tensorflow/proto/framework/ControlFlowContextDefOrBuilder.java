// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/protobuf/control_flow.proto

package org.tensorflow.proto.framework;

public interface ControlFlowContextDefOrBuilder extends
    // @@protoc_insertion_point(interface_extends:tensorflow.ControlFlowContextDef)
    com.google.protobuf.MessageOrBuilder {

  /**
   * <code>.tensorflow.CondContextDef cond_ctxt = 1;</code>
   */
  boolean hasCondCtxt();
  /**
   * <code>.tensorflow.CondContextDef cond_ctxt = 1;</code>
   */
  org.tensorflow.proto.framework.CondContextDef getCondCtxt();
  /**
   * <code>.tensorflow.CondContextDef cond_ctxt = 1;</code>
   */
  org.tensorflow.proto.framework.CondContextDefOrBuilder getCondCtxtOrBuilder();

  /**
   * <code>.tensorflow.WhileContextDef while_ctxt = 2;</code>
   */
  boolean hasWhileCtxt();
  /**
   * <code>.tensorflow.WhileContextDef while_ctxt = 2;</code>
   */
  org.tensorflow.proto.framework.WhileContextDef getWhileCtxt();
  /**
   * <code>.tensorflow.WhileContextDef while_ctxt = 2;</code>
   */
  org.tensorflow.proto.framework.WhileContextDefOrBuilder getWhileCtxtOrBuilder();

  public org.tensorflow.proto.framework.ControlFlowContextDef.CtxtCase getCtxtCase();
}
