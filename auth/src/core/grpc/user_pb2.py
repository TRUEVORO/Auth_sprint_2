# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\nuser.proto\"!\n\x10UserTokenRequest\x12\r\n\x05token\x18\x01 \x01(\t\"(\n\x0cUserResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04role\x18\x07 \x01(\t2@\n\x08\x44\x65tailer\x12\x34\n\x0e\x44\x65tailsByToken\x12\x11.UserTokenRequest\x1a\r.UserResponse\"\x00\x62\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _USERTOKENREQUEST._serialized_start = 14
    _USERTOKENREQUEST._serialized_end = 47
    _USERRESPONSE._serialized_start = 49
    _USERRESPONSE._serialized_end = 89
    _DETAILER._serialized_start = 91
    _DETAILER._serialized_end = 155
# @@protoc_insertion_point(module_scope)
