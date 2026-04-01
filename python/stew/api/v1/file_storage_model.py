# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   file_storage_model.py
@Time    :   2026-04-01 13:40:07
@Desc    :   Generated Pydantic models from protobuf definitions
"""

import datetime
from enum import Enum as _Enum
from google.protobuf import message as _message, message_factory
from protobuf_pydantic_gen.ext import model2protobuf, pool, protobuf2model
from pydantic import BaseModel, ConfigDict, Field as _Field
from typing import List, Optional, Type


class UploadSessionStatus(_Enum):
    UPLOAD_SESSION_STATUS_UNSPECIFIED = 0
    UPLOAD_SESSION_STATUS_ACTIVE = 1
    UPLOAD_SESSION_STATUS_COMPLETED = 2
    UPLOAD_SESSION_STATUS_ABORTED = 3


class UploadFileRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    metadata: Optional[UploadFileMetadata] = _Field(default=None)
    chunk_data: Optional[bytes] = _Field(default=b"")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.UploadFileRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "UploadFileRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class UploadFileMetadata(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    filename: Optional[str] = _Field(default="")
    content_type: Optional[str] = _Field(default="")
    folder: Optional[str] = _Field(default="")
    business_context: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.UploadFileMetadata")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "UploadFileMetadata":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class UploadFileResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    file_info: Optional[FileInfo] = _Field(default=None)
    callback_result: Optional[CallbackResult] = _Field(default=None)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.UploadFileResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "UploadFileResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class InitResumableUploadRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    filename: Optional[str] = _Field(default="")
    content_type: Optional[str] = _Field(default="")
    folder: Optional[str] = _Field(default="")
    total_size: Optional[int] = _Field(default=0)
    part_size: Optional[int] = _Field(default=0)
    business_context: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.InitResumableUploadRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "InitResumableUploadRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class InitResumableUploadResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    upload_id: Optional[str] = _Field(default="")
    part_size: Optional[int] = _Field(default=0)
    total_parts: Optional[int] = _Field(default=0)
    expires_at: Optional[datetime.datetime] = _Field(default=None)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.InitResumableUploadResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "InitResumableUploadResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class UploadPartRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    header: Optional[UploadPartHeader] = _Field(default=None)
    chunk_data: Optional[bytes] = _Field(default=b"")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.UploadPartRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "UploadPartRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class UploadPartHeader(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    upload_id: Optional[str] = _Field(default="")
    part_number: Optional[int] = _Field(default=0)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.UploadPartHeader")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "UploadPartHeader":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class UploadPartResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    part_number: Optional[int] = _Field(default=0)
    etag: Optional[str] = _Field(default="")
    bytes_written: Optional[int] = _Field(default=0)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.UploadPartResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "UploadPartResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class CompleteResumableUploadRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    upload_id: Optional[str] = _Field(default="")
    parts: Optional[List[PartEtag]] = _Field(default=None)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName(
            "stew.api.v1.CompleteResumableUploadRequest"
        )
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "CompleteResumableUploadRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class PartEtag(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    part_number: Optional[int] = _Field(default=0)
    etag: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.PartEtag")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "PartEtag":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class AbortResumableUploadRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    upload_id: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.AbortResumableUploadRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "AbortResumableUploadRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class GetUploadStatusRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    upload_id: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.GetUploadStatusRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "GetUploadStatusRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class GetUploadStatusResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    upload_id: Optional[str] = _Field(default="")
    status: Optional[UploadSessionStatus] = _Field(default=UploadSessionStatus(0))
    completed_parts: Optional[List[UploadedPartInfo]] = _Field(default=None)
    total_parts: Optional[int] = _Field(default=0)
    expires_at: Optional[datetime.datetime] = _Field(default=None)
    filename: Optional[str] = _Field(default="")
    total_size: Optional[int] = _Field(default=0)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.GetUploadStatusResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "GetUploadStatusResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class UploadedPartInfo(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    part_number: Optional[int] = _Field(default=0)
    etag: Optional[str] = _Field(default="")
    size: Optional[int] = _Field(default=0)
    completed_at: Optional[datetime.datetime] = _Field(default=None)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.UploadedPartInfo")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "UploadedPartInfo":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class DownloadFileRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    file_id: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.DownloadFileRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "DownloadFileRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class DownloadFileHttpMetadata(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    filename: Optional[str] = _Field(default="")
    content_disposition: Optional[str] = _Field(default="")
    etag: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.DownloadFileHttpMetadata")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "DownloadFileHttpMetadata":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class DownloadFileChunk(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    data: Optional[bytes] = _Field(default=b"")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.DownloadFileChunk")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "DownloadFileChunk":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class DeleteFileRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    file_id: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.DeleteFileRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "DeleteFileRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class ListFilesRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    folder: Optional[str] = _Field(default="")
    page_size: Optional[int] = _Field(default=0)
    page_token: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.ListFilesRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "ListFilesRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class ListFilesResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    files: Optional[List[FileInfo]] = _Field(default=None)
    next_page_token: Optional[str] = _Field(default="")
    total_count: Optional[int] = _Field(default=0)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.ListFilesResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "ListFilesResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class GetFileInfoRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    file_id: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.GetFileInfoRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "GetFileInfoRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class CallbackResult(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    accepted: Optional[bool] = _Field(default=False)
    business_id: Optional[str] = _Field(default="")
    message: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.CallbackResult")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "CallbackResult":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class FileInfo(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    id: Optional[str] = _Field(default="")
    filename: Optional[str] = _Field(default="")
    content_type: Optional[str] = _Field(default="")
    file_size: Optional[int] = _Field(default=0)
    folder: Optional[str] = _Field(default="")
    owner_id: Optional[str] = _Field(default="")
    checksum: Optional[str] = _Field(default="")
    storage_backend: Optional[str] = _Field(default="")
    created_at: Optional[datetime.datetime] = _Field(default=None)
    updated_at: Optional[datetime.datetime] = _Field(default=None)
    local_path: Optional[str] = _Field(default="")
    storage_key: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.FileInfo")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "FileInfo":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)
