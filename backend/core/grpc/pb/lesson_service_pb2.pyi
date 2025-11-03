import lesson_pb2 as _lesson_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import (
    Iterable as _Iterable,
    Mapping as _Mapping,
)
from typing import (
    ClassVar as _ClassVar,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class StudentAttendanceRequest(_message.Message):
    __slots__ = ("student_id", "attendance")
    STUDENT_ID_FIELD_NUMBER: _ClassVar[int]
    ATTENDANCE_FIELD_NUMBER: _ClassVar[int]
    student_id: str
    attendance: _lesson_pb2.Attendance
    def __init__(
        self,
        student_id: _Optional[str] = ...,
        attendance: _Optional[
            _Union[_lesson_pb2.Attendance, _Mapping]
        ] = ...,
    ) -> None: ...

class StudentAttendanceResponse(_message.Message):
    __slots__ = ("student_id", "attendance")
    STUDENT_ID_FIELD_NUMBER: _ClassVar[int]
    ATTENDANCE_FIELD_NUMBER: _ClassVar[int]
    student_id: str
    attendance: _lesson_pb2.Attendance
    def __init__(
        self,
        student_id: _Optional[str] = ...,
        attendance: _Optional[
            _Union[_lesson_pb2.Attendance, _Mapping]
        ] = ...,
    ) -> None: ...

class LessonsRequest(_message.Message):
    __slots__ = ("date",)
    DATE_FIELD_NUMBER: _ClassVar[int]
    date: str
    def __init__(self, date: _Optional[str] = ...) -> None: ...

class LessonsResponse(_message.Message):
    __slots__ = ("lessons",)
    LESSONS_FIELD_NUMBER: _ClassVar[int]
    lessons: _containers.RepeatedCompositeFieldContainer[
        _lesson_pb2.Schedule
    ]
    def __init__(
        self,
        lessons: _Optional[
            _Iterable[_Union[_lesson_pb2.Schedule, _Mapping]]
        ] = ...,
    ) -> None: ...

class LessonDetailsRequest(_message.Message):
    __slots__ = ("schedule_id",)
    SCHEDULE_ID_FIELD_NUMBER: _ClassVar[int]
    schedule_id: str
    def __init__(
        self, schedule_id: _Optional[str] = ...
    ) -> None: ...

class LessonsForMonthRequest(_message.Message):
    __slots__ = ("month", "year")
    MONTH_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    month: int
    year: int
    def __init__(
        self, month: _Optional[int] = ..., year: _Optional[int] = ...
    ) -> None: ...

class LessonsForMonthResponse(_message.Message):
    __slots__ = ("dates",)
    DATES_FIELD_NUMBER: _ClassVar[int]
    dates: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, dates: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class LessonDetailsResponse(_message.Message):
    __slots__ = ("schedule_data", "groups")
    SCHEDULE_DATA_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    schedule_data: _lesson_pb2.Schedule
    groups: _containers.RepeatedCompositeFieldContainer[
        _lesson_pb2.GroupLesson
    ]
    def __init__(
        self,
        schedule_data: _Optional[
            _Union[_lesson_pb2.Schedule, _Mapping]
        ] = ...,
        groups: _Optional[
            _Iterable[_Union[_lesson_pb2.GroupLesson, _Mapping]]
        ] = ...,
    ) -> None: ...
