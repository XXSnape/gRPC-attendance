from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LessonData(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class Schedule(_message.Message):
    __slots__ = ("number", "type_of_lesson", "subgroup_number", "lesson", "status", "time")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    TYPE_OF_LESSON_FIELD_NUMBER: _ClassVar[int]
    SUBGROUP_NUMBER_FIELD_NUMBER: _ClassVar[int]
    LESSON_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    number: int
    type_of_lesson: str
    subgroup_number: int
    lesson: LessonData
    status: str
    time: str
    def __init__(self, number: _Optional[int] = ..., type_of_lesson: _Optional[str] = ..., subgroup_number: _Optional[int] = ..., lesson: _Optional[_Union[LessonData, _Mapping]] = ..., status: _Optional[str] = ..., time: _Optional[str] = ...) -> None: ...
