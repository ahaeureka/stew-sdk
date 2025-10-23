# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   user_model.py
@Time    :   2025-10-22 08:37:13
@Desc    :   Generated Pydantic models from protobuf definitions
"""

from enum import Enum as _Enum
from google.protobuf import message as _message, message_factory
from protobuf_pydantic_gen.ext import model2protobuf, pool, protobuf2model
from pydantic import BaseModel, ConfigDict, Field as _Field
from typing import Any, Dict, List, Optional, Type


class Role(_Enum):
    ADMIN = 0


class USER_STATUS(_Enum):
    ACTIVE = 0
    INACTIVE = 1
    LOCKED = 2
    DELETED = 3


class UserSvrCode(_Enum):
    USER_UNKNOWN = 0
    USER_LOGIN_ERR = 4107
    USER_TOKEN_EXPIRE_ERR = 4108
    USER_DISABLED_ERR = 4119
    USER_TOKEN_INVALIDATE_ERR = 4109
    USER_TOKEN_NOT_ACTIVTE_ERR = 4114
    USER_AUTH_DECRYPT_ERR = 4110
    USER_ACCOUNT_ERR = 4111
    USER_PASSWORD_ERR = 4112
    USER_NOT_FOUND_ERR = 4113
    USER_AUTH_MISSING_ERR = 4115
    USER_IDENTITY_MISSING_ERR = 4116
    USER_APIKEY_NOT_MATCH_ERR = 4117
    USER_USERNAME_DUPLICATE_ERR = 4118


class Address(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    formatted: Optional[str] = _Field(default="")
    street_address: Optional[str] = _Field(default="")
    locality: Optional[str] = _Field(default="")
    region: Optional[str] = _Field(default="")
    postal_code: Optional[str] = _Field(default="")
    country: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.Address")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "Address":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class User(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    sub: Optional[str] = _Field(default="")
    name: Optional[str] = _Field(default="")
    given_name: Optional[str] = _Field(default="")
    family_name: Optional[str] = _Field(default="")
    middle_name: Optional[str] = _Field(default="")
    nickname: Optional[str] = _Field(default="")
    preferred_username: Optional[str] = _Field(default="")
    profile: Optional[str] = _Field(default="")
    picture: Optional[str] = _Field(default="")
    website: Optional[str] = _Field(default="")
    email: Optional[str] = _Field(default="")
    email_verified: Optional[bool] = _Field(default=False)
    gender: Optional[str] = _Field(default="")
    birthdate: Optional[str] = _Field(default="")
    zoneinfo: Optional[str] = _Field(default="")
    locale: Optional[str] = _Field(default="")
    phone_number: Optional[str] = _Field(default="")
    phone_number_verified: Optional[bool] = _Field(default=False)
    address: Optional[List[Address]] = _Field(default=None)
    updated_at: Optional[int] = _Field(default=0)
    id: Optional[str] = _Field(default="")
    owner: Optional[str] = _Field(default="")
    type: Optional[str] = _Field(default="")
    password: Optional[str] = _Field(default="")
    password_salt: Optional[str] = _Field(default="")
    password_type: Optional[str] = _Field(default="")
    display_name: Optional[str] = _Field(default="")
    first_name: Optional[str] = _Field(default="")
    last_name: Optional[str] = _Field(default="")
    avatar: Optional[str] = _Field(default="")
    avatar_type: Optional[str] = _Field(default="")
    permanent_avatar: Optional[str] = _Field(default="")
    properties: Optional[Dict[str, Any]] = _Field(default=None)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.User")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "User":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class BasicAuth(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    uid: Optional[str] = _Field(default="")
    name: Optional[str] = _Field(default="")
    role: Optional[Role] = _Field(default=Role(0))
    audience: Optional[str] = _Field(default="")
    issuer: Optional[str] = _Field(default="")
    not_before: Optional[int] = _Field(default=0)
    expiration: Optional[int] = _Field(default=0)
    issued_at: Optional[int] = _Field(default=0)
    is_keep_login: Optional[bool] = _Field(default=False)
    token: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.BasicAuth")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "BasicAuth":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class PostUserRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    name: Optional[str] = _Field(default="")
    password: Optional[str] = _Field(default="")
    email: Optional[str] = _Field(default="")
    phone: Optional[str] = _Field(default="")
    role: Optional[Role] = _Field(default=Role(0))
    status: Optional[USER_STATUS] = _Field(default=USER_STATUS(0))
    dept: Optional[str] = _Field(default="")
    owner: Optional[str] = _Field(default="")
    avatar: Optional[str] = _Field(default="")
    tenant_id: Optional[str] = _Field(default="")
    update_mask: Optional[FieldMask] = _Field(default=None)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.PostUserRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "PostUserRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class GetUserRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    uid: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.GetUserRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "GetUserRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class DeleteUserRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    uid: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.DeleteUserRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "DeleteUserRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class DeleteUserResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    uid: Optional[str] = _Field(default="")

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.DeleteUserResponse")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "DeleteUserResponse":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)


class PatchUserRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    uid: Optional[str] = _Field(default="")
    name: Optional[str] = _Field(default="")
    password: Optional[str] = _Field(default="")
    email: Optional[str] = _Field(default="")
    phone: Optional[str] = _Field(default="")
    role: Optional[Role] = _Field(default=Role(0))
    status: Optional[USER_STATUS] = _Field(default=USER_STATUS(0))
    dept: Optional[str] = _Field(default="")
    owner: Optional[str] = _Field(default="")
    avatar: Optional[str] = _Field(default="")
    update_mask: Optional[FieldMask] = _Field(default=None)

    def to_protobuf(self) -> _message.Message:
        """Convert Pydantic model to protobuf message"""
        _proto = pool.FindMessageTypeByName("stew.api.v1.PatchUserRequest")
        _cls: Type[_message.Message] = message_factory.GetMessageClass(_proto)
        return model2protobuf(self, _cls())

    @classmethod
    def from_protobuf(cls, src: _message.Message) -> "PatchUserRequest":
        """Convert protobuf message to Pydantic model"""
        return protobuf2model(cls, src)
