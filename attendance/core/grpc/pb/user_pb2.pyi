from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserData(_message.Message):
    __slots__ = ("type", "full_name")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    type: str
    full_name: str
    def __init__(
        self,
        type: _Optional[str] = ...,
        full_name: _Optional[str] = ...,
    ) -> None: ...
