import user_pb2 as _user_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

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
    __slots__ = ("id", "name", "on_schedule")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ON_SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    on_schedule: bool
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., on_schedule: bool = ...) -> None: ...

class Attendance(_message.Message):
    __slots__ = ("status", "decryption")
    class AttendanceStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PRESENT: _ClassVar[Attendance.AttendanceStatus]
        ABSENT: _ClassVar[Attendance.AttendanceStatus]
        SKIP_RESPECTFULLY: _ClassVar[Attendance.AttendanceStatus]
    PRESENT: Attendance.AttendanceStatus
    ABSENT: Attendance.AttendanceStatus
    SKIP_RESPECTFULLY: Attendance.AttendanceStatus
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DECRYPTION_FIELD_NUMBER: _ClassVar[int]
    status: Attendance.AttendanceStatus
    decryption: str
    def __init__(self, status: _Optional[_Union[Attendance.AttendanceStatus, str]] = ..., decryption: _Optional[str] = ...) -> None: ...

class StudentAttendance(_message.Message):
    __slots__ = ("full_name", "decryption_of_full_name", "attendance", "personal_number", "is_prefect")
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    DECRYPTION_OF_FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTENDANCE_FIELD_NUMBER: _ClassVar[int]
    PERSONAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    IS_PREFECT_FIELD_NUMBER: _ClassVar[int]
    full_name: str
    decryption_of_full_name: str
    attendance: Attendance
    personal_number: str
    is_prefect: bool
    def __init__(self, full_name: _Optional[str] = ..., decryption_of_full_name: _Optional[str] = ..., attendance: _Optional[_Union[Attendance, _Mapping]] = ..., personal_number: _Optional[str] = ..., is_prefect: bool = ...) -> None: ...

class Group(_message.Message):
    __slots__ = ("complete_name",)
    COMPLETE_NAME_FIELD_NUMBER: _ClassVar[int]
    complete_name: str
    def __init__(self, complete_name: _Optional[str] = ...) -> None: ...

class Schedule(_message.Message):
    __slots__ = ("number", "type_of_lesson", "subgroup_number", "lesson", "attendance", "time", "audience", "teachers", "can_be_edited_by_perfect")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    TYPE_OF_LESSON_FIELD_NUMBER: _ClassVar[int]
    SUBGROUP_NUMBER_FIELD_NUMBER: _ClassVar[int]
    LESSON_FIELD_NUMBER: _ClassVar[int]
    ATTENDANCE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    AUDIENCE_FIELD_NUMBER: _ClassVar[int]
    TEACHERS_FIELD_NUMBER: _ClassVar[int]
    CAN_BE_EDITED_BY_PERFECT_FIELD_NUMBER: _ClassVar[int]
    number: int
    type_of_lesson: str
    subgroup_number: int
    lesson: LessonData
    attendance: Attendance
    time: str
    audience: Audience
    teachers: _containers.RepeatedCompositeFieldContainer[_user_pb2.UserFullName]
    can_be_edited_by_perfect: bool
    def __init__(self, number: _Optional[int] = ..., type_of_lesson: _Optional[str] = ..., subgroup_number: _Optional[int] = ..., lesson: _Optional[_Union[LessonData, _Mapping]] = ..., attendance: _Optional[_Union[Attendance, _Mapping]] = ..., time: _Optional[str] = ..., audience: _Optional[_Union[Audience, _Mapping]] = ..., teachers: _Optional[_Iterable[_Union[_user_pb2.UserFullName, _Mapping]]] = ..., can_be_edited_by_perfect: bool = ...) -> None: ...
