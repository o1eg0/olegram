# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: postservice.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'postservice.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11postservice.proto\x12\x0bpostservice\"\x94\x01\n\x04Post\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x12\n\ncreator_id\x18\x04 \x01(\t\x12\x12\n\ncreated_at\x18\x05 \x01(\t\x12\x12\n\nupdated_at\x18\x06 \x01(\t\x12\x12\n\nis_private\x18\x07 \x01(\x08\x12\x0c\n\x04tags\x18\x08 \x03(\t\"m\n\x11\x43reatePostRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x12\n\ncreator_id\x18\x03 \x01(\t\x12\x12\n\nis_private\x18\x04 \x01(\x08\x12\x0c\n\x04tags\x18\x05 \x03(\t\"5\n\x12\x43reatePostResponse\x12\x1f\n\x04post\x18\x01 \x01(\x0b\x32\x11.postservice.Post\"7\n\x0eGetPostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x14\n\x0crequester_id\x18\x02 \x01(\t\"2\n\x0fGetPostResponse\x12\x1f\n\x04post\x18\x01 \x01(\x0b\x32\x11.postservice.Post\"\x80\x01\n\x11UpdatePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x14\n\x0crequester_id\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x12\n\nis_private\x18\x05 \x01(\x08\x12\x0c\n\x04tags\x18\x06 \x03(\t\"5\n\x12UpdatePostResponse\x12\x1f\n\x04post\x18\x01 \x01(\x0b\x32\x11.postservice.Post\":\n\x11\x44\x65letePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x14\n\x0crequester_id\x18\x02 \x01(\t\"%\n\x12\x44\x65letePostResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"I\n\x10ListPostsRequest\x12\x14\n\x0crequester_id\x18\x01 \x01(\t\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x11\n\tpage_size\x18\x03 \x01(\x05\"J\n\x11ListPostsResponse\x12 \n\x05posts\x18\x01 \x03(\x0b\x32\x11.postservice.Post\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\x32\x8c\x03\n\x0bPostService\x12M\n\nCreatePost\x12\x1e.postservice.CreatePostRequest\x1a\x1f.postservice.CreatePostResponse\x12\x44\n\x07GetPost\x12\x1b.postservice.GetPostRequest\x1a\x1c.postservice.GetPostResponse\x12M\n\nUpdatePost\x12\x1e.postservice.UpdatePostRequest\x1a\x1f.postservice.UpdatePostResponse\x12M\n\nDeletePost\x12\x1e.postservice.DeletePostRequest\x1a\x1f.postservice.DeletePostResponse\x12J\n\tListPosts\x12\x1d.postservice.ListPostsRequest\x1a\x1e.postservice.ListPostsResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'postservice_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_POST']._serialized_start=35
  _globals['_POST']._serialized_end=183
  _globals['_CREATEPOSTREQUEST']._serialized_start=185
  _globals['_CREATEPOSTREQUEST']._serialized_end=294
  _globals['_CREATEPOSTRESPONSE']._serialized_start=296
  _globals['_CREATEPOSTRESPONSE']._serialized_end=349
  _globals['_GETPOSTREQUEST']._serialized_start=351
  _globals['_GETPOSTREQUEST']._serialized_end=406
  _globals['_GETPOSTRESPONSE']._serialized_start=408
  _globals['_GETPOSTRESPONSE']._serialized_end=458
  _globals['_UPDATEPOSTREQUEST']._serialized_start=461
  _globals['_UPDATEPOSTREQUEST']._serialized_end=589
  _globals['_UPDATEPOSTRESPONSE']._serialized_start=591
  _globals['_UPDATEPOSTRESPONSE']._serialized_end=644
  _globals['_DELETEPOSTREQUEST']._serialized_start=646
  _globals['_DELETEPOSTREQUEST']._serialized_end=704
  _globals['_DELETEPOSTRESPONSE']._serialized_start=706
  _globals['_DELETEPOSTRESPONSE']._serialized_end=743
  _globals['_LISTPOSTSREQUEST']._serialized_start=745
  _globals['_LISTPOSTSREQUEST']._serialized_end=818
  _globals['_LISTPOSTSRESPONSE']._serialized_start=820
  _globals['_LISTPOSTSRESPONSE']._serialized_end=894
  _globals['_POSTSERVICE']._serialized_start=897
  _globals['_POSTSERVICE']._serialized_end=1293
# @@protoc_insertion_point(module_scope)
