import lesson_pb2 as _lesson_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LessonsRequest(_message.Message):
    __slots__ = ("date",)
    DATE_FIELD_NUMBER: _ClassVar[int]
    date: str
    def __init__(self, date: _Optional[str] = ...) -> None: ...

class LessonsResponse(_message.Message):
    __slots__ = ("lessons",)
    LESSONS_FIELD_NUMBER: _ClassVar[int]
    lessons: _containers.RepeatedCompositeFieldContainer[_lesson_pb2.Schedule]
    def __init__(self, lessons: _Optional[_Iterable[_Union[_lesson_pb2.Schedule, _Mapping]]] = ...) -> None: ...

class LessonDetailsRequest(_message.Message):
    __slots__ = ("lesson_id",)
    LESSON_ID_FIELD_NUMBER: _ClassVar[int]
    lesson_id: str
    def __init__(self, lesson_id: _Optional[str] = ...) -> None: ...

class LessonsForMonthRequest(_message.Message):
    __slots__ = ("month", "year")
    MONTH_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    month: int
    year: int
    def __init__(self, month: _Optional[int] = ..., year: _Optional[int] = ...) -> None: ...

class LessonsForMonthResponse(_message.Message):
    __slots__ = ("dates",)
    DATES_FIELD_NUMBER: _ClassVar[int]
    dates: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, dates: _Optional[_Iterable[str]] = ...) -> None: ...

class LessonDetailsResponse(_message.Message):
    __slots__ = ("schedule_data", "group", "attendances")
    SCHEDULE_DATA_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    ATTENDANCES_FIELD_NUMBER: _ClassVar[int]
    schedule_data: _lesson_pb2.Schedule
    group: _lesson_pb2.Group
    attendances: _containers.RepeatedCompositeFieldContainer[_lesson_pb2.StudentAttendance]
    def __init__(self, schedule_data: _Optional[_Union[_lesson_pb2.Schedule, _Mapping]] = ..., group: _Optional[_Union[_lesson_pb2.Group, _Mapping]] = ..., attendances: _Optional[_Iterable[_Union[_lesson_pb2.StudentAttendance, _Mapping]]] = ...) -> None: ...
