from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

import user_pb2 as _user_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Address(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Audience(_message.Message):
    __slots__ = ("name", "address")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    name: str
    address: Address
    def __init__(self, name: _Optional[str] = ..., address: _Optional[_Union[Address, _Mapping]] = ...) -> None: ...

class LessonData(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class Schedule(_message.Message):
    __slots__ = ("number", "type_of_lesson", "subgroup_number", "lesson", "status", "time", "audience", "teachers")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    TYPE_OF_LESSON_FIELD_NUMBER: _ClassVar[int]
    SUBGROUP_NUMBER_FIELD_NUMBER: _ClassVar[int]
    LESSON_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    AUDIENCE_FIELD_NUMBER: _ClassVar[int]
    TEACHERS_FIELD_NUMBER: _ClassVar[int]
    number: int
    type_of_lesson: str
    subgroup_number: int
    lesson: LessonData
    status: str
    time: str
    audience: Audience
    teachers: _containers.RepeatedCompositeFieldContainer[_user_pb2.UserFullName]
    def __init__(self, number: _Optional[int] = ..., type_of_lesson: _Optional[str] = ..., subgroup_number: _Optional[int] = ..., lesson: _Optional[_Union[LessonData, _Mapping]] = ..., status: _Optional[str] = ..., time: _Optional[str] = ..., audience: _Optional[_Union[Audience, _Mapping]] = ..., teachers: _Optional[_Iterable[_Union[_user_pb2.UserFullName, _Mapping]]] = ...) -> None: ...
