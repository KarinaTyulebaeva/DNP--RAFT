# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: raft.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nraft.proto\"7\n\x12RequestVoteRequest\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x13\n\x0b\x63\x61ndidateId\x18\x02 \x01(\x05\"3\n\x13RequestVoteResponse\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0e\n\x06result\x18\x02 \x01(\x08\"5\n\x12\x41ppendEntryRequest\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x11\n\tleaaderId\x18\x02 \x01(\x05\"6\n\x15\x41ppendEntriesResponse\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x08\"\x0e\n\x0c\x45mptyRequest\"\"\n\x0fSuspendResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"6\n\x11GetLeaderResponse\x12\x10\n\x08leaderId\x18\x01 \x01(\x05\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\" \n\x0eSuspendRequest\x12\x0e\n\x06period\x18\x01 \x01(\x05\x32\xe3\x01\n\x0bRaftService\x12\x38\n\x0bRequestVote\x12\x13.RequestVoteRequest\x1a\x14.RequestVoteResponse\x12<\n\rAppendEntries\x12\x13.AppendEntryRequest\x1a\x16.AppendEntriesResponse\x12.\n\tGetLeader\x12\r.EmptyRequest\x1a\x12.GetLeaderResponse\x12,\n\x07Suspend\x12\x0f.SuspendRequest\x1a\x10.SuspendResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'raft_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUESTVOTEREQUEST._serialized_start=14
  _REQUESTVOTEREQUEST._serialized_end=69
  _REQUESTVOTERESPONSE._serialized_start=71
  _REQUESTVOTERESPONSE._serialized_end=122
  _APPENDENTRYREQUEST._serialized_start=124
  _APPENDENTRYREQUEST._serialized_end=177
  _APPENDENTRIESRESPONSE._serialized_start=179
  _APPENDENTRIESRESPONSE._serialized_end=233
  _EMPTYREQUEST._serialized_start=235
  _EMPTYREQUEST._serialized_end=249
  _SUSPENDRESPONSE._serialized_start=251
  _SUSPENDRESPONSE._serialized_end=285
  _GETLEADERRESPONSE._serialized_start=287
  _GETLEADERRESPONSE._serialized_end=341
  _SUSPENDREQUEST._serialized_start=343
  _SUSPENDREQUEST._serialized_end=375
  _RAFTSERVICE._serialized_start=378
  _RAFTSERVICE._serialized_end=605
# @@protoc_insertion_point(module_scope)
