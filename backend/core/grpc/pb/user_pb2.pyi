from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserData(_message.Message):
    __slots__ = ("id", "role", "full_name")
    ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    role: str
    full_name: str
    def __init__(self, id: _Optional[str] = ..., role: _Optional[str] = ..., full_name: _Optional[str] = ...) -> None: ...

class UserFullName(_message.Message):
    __slots__ = ("full_name", "decryption_of_full_name")
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    DECRYPTION_OF_FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    full_name: str
    decryption_of_full_name: str
    def __init__(self, full_name: _Optional[str] = ..., decryption_of_full_name: _Optional[str] = ...) -> None: ...
