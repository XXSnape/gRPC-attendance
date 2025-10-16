from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class UserData(_message.Message):
    __slots__ = ("id", "type", "full_name")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    full_name: str
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., full_name: _Optional[str] = ...) -> None: ...

class UserFullName(_message.Message):
    __slots__ = ("full_name",)
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    full_name: str
    def __init__(self, full_name: _Optional[str] = ...) -> None: ...
