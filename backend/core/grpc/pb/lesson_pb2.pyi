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
    __slots__ = ("student_id", "full_name", "decryption_of_full_name", "attendance", "personal_number", "is_prefect")
    STUDENT_ID_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    DECRYPTION_OF_FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTENDANCE_FIELD_NUMBER: _ClassVar[int]
    PERSONAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    IS_PREFECT_FIELD_NUMBER: _ClassVar[int]
    student_id: str
    full_name: str
    decryption_of_full_name: str
    attendance: Attendance
    personal_number: str
    is_prefect: bool
    def __init__(self, student_id: _Optional[str] = ..., full_name: _Optional[str] = ..., decryption_of_full_name: _Optional[str] = ..., attendance: _Optional[_Union[Attendance, _Mapping]] = ..., personal_number: _Optional[str] = ..., is_prefect: bool = ...) -> None: ...

class GroupLesson(_message.Message):
    __slots__ = ("id", "complete_name", "attendances", "can_be_edited_by_prefect")
    ID_FIELD_NUMBER: _ClassVar[int]
    COMPLETE_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTENDANCES_FIELD_NUMBER: _ClassVar[int]
    CAN_BE_EDITED_BY_PREFECT_FIELD_NUMBER: _ClassVar[int]
    id: str
    complete_name: str
    attendances: _containers.RepeatedCompositeFieldContainer[StudentAttendance]
    can_be_edited_by_prefect: bool
    def __init__(self, id: _Optional[str] = ..., complete_name: _Optional[str] = ..., attendances: _Optional[_Iterable[_Union[StudentAttendance, _Mapping]]] = ..., can_be_edited_by_prefect: bool = ...) -> None: ...

class StudentLesson(_message.Message):
    __slots__ = ("attendance", "group_id", "is_prefect")
    ATTENDANCE_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PREFECT_FIELD_NUMBER: _ClassVar[int]
    attendance: Attendance
    group_id: str
    is_prefect: bool
    def __init__(self, attendance: _Optional[_Union[Attendance, _Mapping]] = ..., group_id: _Optional[str] = ..., is_prefect: bool = ...) -> None: ...

class TotalAttendance(_message.Message):
    __slots__ = ("total_students", "present_students")
    TOTAL_STUDENTS_FIELD_NUMBER: _ClassVar[int]
    PRESENT_STUDENTS_FIELD_NUMBER: _ClassVar[int]
    total_students: int
    present_students: int
    def __init__(self, total_students: _Optional[int] = ..., present_students: _Optional[int] = ...) -> None: ...

class Schedule(_message.Message):
    __slots__ = ("id", "number", "date", "type_of_lesson", "subgroup_number", "lesson", "student_data", "time", "audiences", "teachers", "can_be_edited_by_prefect", "group_names", "total_attendance")
    ID_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    TYPE_OF_LESSON_FIELD_NUMBER: _ClassVar[int]
    SUBGROUP_NUMBER_FIELD_NUMBER: _ClassVar[int]
    LESSON_FIELD_NUMBER: _ClassVar[int]
    STUDENT_DATA_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    AUDIENCES_FIELD_NUMBER: _ClassVar[int]
    TEACHERS_FIELD_NUMBER: _ClassVar[int]
    CAN_BE_EDITED_BY_PREFECT_FIELD_NUMBER: _ClassVar[int]
    GROUP_NAMES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ATTENDANCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    number: int
    date: str
    type_of_lesson: str
    subgroup_number: int
    lesson: LessonData
    student_data: StudentLesson
    time: str
    audiences: _containers.RepeatedCompositeFieldContainer[Audience]
    teachers: _containers.RepeatedCompositeFieldContainer[_user_pb2.UserFullName]
    can_be_edited_by_prefect: bool
    group_names: _containers.RepeatedScalarFieldContainer[str]
    total_attendance: TotalAttendance
    def __init__(self, id: _Optional[str] = ..., number: _Optional[int] = ..., date: _Optional[str] = ..., type_of_lesson: _Optional[str] = ..., subgroup_number: _Optional[int] = ..., lesson: _Optional[_Union[LessonData, _Mapping]] = ..., student_data: _Optional[_Union[StudentLesson, _Mapping]] = ..., time: _Optional[str] = ..., audiences: _Optional[_Iterable[_Union[Audience, _Mapping]]] = ..., teachers: _Optional[_Iterable[_Union[_user_pb2.UserFullName, _Mapping]]] = ..., can_be_edited_by_prefect: bool = ..., group_names: _Optional[_Iterable[str]] = ..., total_attendance: _Optional[_Union[TotalAttendance, _Mapping]] = ...) -> None: ...
