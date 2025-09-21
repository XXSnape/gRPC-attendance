from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("name", "age", "sex")
    class Sex(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MALE: _ClassVar[User.Sex]
        FEMALE: _ClassVar[User.Sex]
    MALE: User.Sex
    FEMALE: User.Sex
    NAME_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    SEX_FIELD_NUMBER: _ClassVar[int]
    name: str
    age: int
    sex: User.Sex
    def __init__(self, name: _Optional[str] = ..., age: _Optional[int] = ..., sex: _Optional[_Union[User.Sex, str]] = ...) -> None: ...
