import datetime
import uuid

from core.databases.sql.models.enums.type_of_lesson import (
    TypeOfLessonEnum,
)
from pydantic import computed_field

from .address import AudienceSchema
from .attendance import AttendanceSchema
from .common import BaseSchema, IdSchema
from .user import UserFullNameSchema, UserAttendanceSchema


class BaseLessonSchema(BaseSchema):
    id: uuid.UUID
    name: str
    on_schedule: bool


class StudentLessonSchema(BaseSchema):
    attendance: AttendanceSchema
    group_id: uuid.UUID | str
    is_prefect: bool | None = None


class BaseScheduleSchema(IdSchema):
    number: int
    date: datetime.date
    type_of_lesson: TypeOfLessonEnum
    subgroup_number: int | None
    lesson: BaseLessonSchema
    audience: AudienceSchema
    student_data: StudentLessonSchema | None
    teachers: list[UserFullNameSchema]
    can_be_edited_by_prefect: bool | None = None

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
