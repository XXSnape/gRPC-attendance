from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

import lesson_pb2 as _lesson_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class SelfApproveLessonAttendanceRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class LessonQRCodeResponse(_message.Message):
    __slots__ = ("qr_url", "token", "total_attendance", "expires_at")
    QR_URL_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ATTENDANCE_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    qr_url: str
    token: str
    total_attendance: _lesson_pb2.TotalAttendance
    expires_at: str
    def __init__(
        self,
        qr_url: _Optional[str] = ...,
        token: _Optional[str] = ...,
        total_attendance: _Optional[
            _Union[_lesson_pb2.TotalAttendance, _Mapping]
        ] = ...,
        expires_at: _Optional[str] = ...,
    ) -> None: ...

class GrantPrefectAttendancePermissionsRequest(_message.Message):
    __slots__ = (
        "schedule_id",
        "number_of_minutes_of_access",
        "group_id",
    )
    SCHEDULE_ID_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_MINUTES_OF_ACCESS_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    schedule_id: str
    number_of_minutes_of_access: int
    group_id: str
    def __init__(
        self,
        schedule_id: _Optional[str] = ...,
        number_of_minutes_of_access: _Optional[int] = ...,
        group_id: _Optional[str] = ...,
    ) -> None: ...

class OkResponse(_message.Message):
    __slots__ = ("ok",)
    OK_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    def __init__(self, ok: bool = ...) -> None: ...

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
