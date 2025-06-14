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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11postservice.proto\x12\x0bpostservice\"\xb2\x01\n\x04Post\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x12\n\ncreator_id\x18\x04 \x01(\t\x12\x12\n\ncreated_at\x18\x05 \x01(\t\x12\x12\n\nupdated_at\x18\x06 \x01(\t\x12\x12\n\nis_private\x18\x07 \x01(\x08\x12\x0c\n\x04tags\x18\x08 \x03(\t\x12\r\n\x05views\x18\t \x01(\x03\x12\r\n\x05likes\x18\n \x01(\x03\"m\n\x11\x43reatePostRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x12\n\ncreator_id\x18\x03 \x01(\t\x12\x12\n\nis_private\x18\x04 \x01(\x08\x12\x0c\n\x04tags\x18\x05 \x03(\t\"5\n\x12\x43reatePostResponse\x12\x1f\n\x04post\x18\x01 \x01(\x0b\x32\x11.postservice.Post\"7\n\x0eGetPostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x14\n\x0crequester_id\x18\x02 \x01(\t\"2\n\x0fGetPostResponse\x12\x1f\n\x04post\x18\x01 \x01(\x0b\x32\x11.postservice.Post\"\x80\x01\n\x11UpdatePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x14\n\x0crequester_id\x18\x02 \x01(\t\x12\r\n\x05title\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x12\n\nis_private\x18\x05 \x01(\x08\x12\x0c\n\x04tags\x18\x06 \x03(\t\"5\n\x12UpdatePostResponse\x12\x1f\n\x04post\x18\x01 \x01(\x0b\x32\x11.postservice.Post\":\n\x11\x44\x65letePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x14\n\x0crequester_id\x18\x02 \x01(\t\"%\n\x12\x44\x65letePostResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"]\n\x10ListPostsRequest\x12\x14\n\x0crequester_id\x18\x01 \x01(\t\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x11\n\tpage_size\x18\x03 \x01(\x05\x12\x12\n\ncreator_id\x18\x04 \x01(\t\"J\n\x11ListPostsResponse\x12 \n\x05posts\x18\x01 \x03(\x0b\x32\x11.postservice.Post\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"5\n\x0fViewPostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x11\n\tviewer_id\x18\x02 \x01(\t\"#\n\x10ViewPostResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"3\n\x0fLikePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\"#\n\x10LikePostResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"Y\n\x07\x43omment\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07post_id\x18\x02 \x01(\t\x12\x0f\n\x07user_id\x18\x03 \x01(\t\x12\x0c\n\x04text\x18\x04 \x01(\t\x12\x12\n\ncreated_at\x18\x05 \x01(\t\"C\n\x11\x41\x64\x64\x43ommentRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x0c\n\x04text\x18\x03 \x01(\t\";\n\x12\x41\x64\x64\x43ommentResponse\x12%\n\x07\x63omment\x18\x01 \x01(\x0b\x32\x14.postservice.Comment\"F\n\x12GetCommentsRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x11\n\tpage_size\x18\x03 \x01(\x05\"R\n\x13GetCommentsResponse\x12&\n\x08\x63omments\x18\x01 \x03(\x0b\x32\x14.postservice.Comment\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\x32\xbf\x05\n\x0bPostService\x12M\n\nCreatePost\x12\x1e.postservice.CreatePostRequest\x1a\x1f.postservice.CreatePostResponse\x12\x44\n\x07GetPost\x12\x1b.postservice.GetPostRequest\x1a\x1c.postservice.GetPostResponse\x12M\n\nUpdatePost\x12\x1e.postservice.UpdatePostRequest\x1a\x1f.postservice.UpdatePostResponse\x12M\n\nDeletePost\x12\x1e.postservice.DeletePostRequest\x1a\x1f.postservice.DeletePostResponse\x12J\n\tListPosts\x12\x1d.postservice.ListPostsRequest\x1a\x1e.postservice.ListPostsResponse\x12G\n\x08ViewPost\x12\x1c.postservice.ViewPostRequest\x1a\x1d.postservice.ViewPostResponse\x12G\n\x08LikePost\x12\x1c.postservice.LikePostRequest\x1a\x1d.postservice.LikePostResponse\x12M\n\nAddComment\x12\x1e.postservice.AddCommentRequest\x1a\x1f.postservice.AddCommentResponse\x12P\n\x0bGetComments\x12\x1f.postservice.GetCommentsRequest\x1a .postservice.GetCommentsResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'postservice_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_POST']._serialized_start=35
  _globals['_POST']._serialized_end=213
  _globals['_CREATEPOSTREQUEST']._serialized_start=215
  _globals['_CREATEPOSTREQUEST']._serialized_end=324
  _globals['_CREATEPOSTRESPONSE']._serialized_start=326
  _globals['_CREATEPOSTRESPONSE']._serialized_end=379
  _globals['_GETPOSTREQUEST']._serialized_start=381
  _globals['_GETPOSTREQUEST']._serialized_end=436
  _globals['_GETPOSTRESPONSE']._serialized_start=438
  _globals['_GETPOSTRESPONSE']._serialized_end=488
  _globals['_UPDATEPOSTREQUEST']._serialized_start=491
  _globals['_UPDATEPOSTREQUEST']._serialized_end=619
  _globals['_UPDATEPOSTRESPONSE']._serialized_start=621
  _globals['_UPDATEPOSTRESPONSE']._serialized_end=674
  _globals['_DELETEPOSTREQUEST']._serialized_start=676
  _globals['_DELETEPOSTREQUEST']._serialized_end=734
  _globals['_DELETEPOSTRESPONSE']._serialized_start=736
  _globals['_DELETEPOSTRESPONSE']._serialized_end=773
  _globals['_LISTPOSTSREQUEST']._serialized_start=775
  _globals['_LISTPOSTSREQUEST']._serialized_end=868
  _globals['_LISTPOSTSRESPONSE']._serialized_start=870
  _globals['_LISTPOSTSRESPONSE']._serialized_end=944
  _globals['_VIEWPOSTREQUEST']._serialized_start=946
  _globals['_VIEWPOSTREQUEST']._serialized_end=999
  _globals['_VIEWPOSTRESPONSE']._serialized_start=1001
  _globals['_VIEWPOSTRESPONSE']._serialized_end=1036
  _globals['_LIKEPOSTREQUEST']._serialized_start=1038
  _globals['_LIKEPOSTREQUEST']._serialized_end=1089
  _globals['_LIKEPOSTRESPONSE']._serialized_start=1091
  _globals['_LIKEPOSTRESPONSE']._serialized_end=1126
  _globals['_COMMENT']._serialized_start=1128
  _globals['_COMMENT']._serialized_end=1217
  _globals['_ADDCOMMENTREQUEST']._serialized_start=1219
  _globals['_ADDCOMMENTREQUEST']._serialized_end=1286
  _globals['_ADDCOMMENTRESPONSE']._serialized_start=1288
  _globals['_ADDCOMMENTRESPONSE']._serialized_end=1347
  _globals['_GETCOMMENTSREQUEST']._serialized_start=1349
  _globals['_GETCOMMENTSREQUEST']._serialized_end=1419
  _globals['_GETCOMMENTSRESPONSE']._serialized_start=1421
  _globals['_GETCOMMENTSRESPONSE']._serialized_end=1503
  _globals['_POSTSERVICE']._serialized_start=1506
  _globals['_POSTSERVICE']._serialized_end=2209
# @@protoc_insertion_point(module_scope)
