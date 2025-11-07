import datetime
import uuid
from typing import Annotated

from core.databases.sql.models.enums.type_of_lesson import (
    TypeOfLessonEnum,
)
from pydantic import computed_field, Field, HttpUrl

from .address import AudienceSchema
from .attendance import AttendanceSchema
from .common import BaseSchema, IdSchema
from .user import UserAttendanceSchema, UserFullNameSchema
from .validators.grpc_converter import gRPCValidator


class BaseLessonSchema(BaseSchema):
    id: uuid.UUID
    name: str


class StudentLessonSchema(BaseSchema):
    attendance: AttendanceSchema
    group_id: uuid.UUID
    is_prefect: bool | None = None


class TotalAttendance(BaseSchema):
    total_students: int
    present_students: int


class BaseScheduleSchema(IdSchema):
    number: int
    date: datetime.date
    type_of_lesson: TypeOfLessonEnum
    is_standardized: bool
    subgroup_number: int | None
    lesson: BaseLessonSchema
    audiences: list[AudienceSchema]
    student_data: Annotated[
        StudentLessonSchema | None,
        gRPCValidator,
    ]
    teachers: list[UserFullNameSchema]
    group_names: list[str]
    can_be_edited_by_prefect: bool | None = None
    total_attendance: Annotated[
        TotalAttendance | None,
        gRPCValidator,
    ]

    @computed_field
    @property
    def time(self) -> str:
        return {
            1: "09:00 - 10:30",
            2: "10:40 - 12:10",
            3: "12:40 - 14:10",
            4: "14:20 - 15:50",
            5: "16:20 - 17:50",
            6: "18:00 - 19:30",
            7: "20:00 - 21:30",
        }[self.number]


class LessonsDataSchema(BaseSchema):
    lessons: list[BaseScheduleSchema]


class GroupSchema(IdSchema):
    complete_name: str
    attendances: list[UserAttendanceSchema]
    can_be_edited_by_prefect: bool | None = False


class LessonQRCodeDataSchema(BaseSchema):
    qr_url: HttpUrl
    token: str
    total_attendance: TotalAttendance
    expires_at: datetime.datetime


class FullScheduleDataSchema(BaseSchema):
    schedule_data: BaseScheduleSchema
    groups: list[GroupSchema]


class StudyDaysSchema(BaseSchema):
    dates: list[datetime.date]


class MarkStudentAttendanceSchema(BaseSchema):
    student_id: uuid.UUID
    attendance: AttendanceSchema


class ReadLessonStudentAttendanceSchema(BaseSchema):
    attendances: list[MarkStudentAttendanceSchema]


class GrantPrefectRightsSchema(BaseSchema):
    number_of_minutes_of_access: Annotated[
        int | None, Field(ge=1, le=90)
    ]
