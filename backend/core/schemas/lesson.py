import uuid

from core.databases.sql.models.enums.type_of_lesson import (
    TypeOfLessonEnum,
)
from core.enums.status import AttendanceStatus
from pydantic import computed_field

from .address import AudienceSchema
from .common import BaseSchema
from .user import UserFullNameSchema


class BaseLessonSchema(BaseSchema):
    id: uuid.UUID
    name: str


class BaseScheduleSchema(BaseSchema):
    number: int
    type_of_lesson: TypeOfLessonEnum
    subgroup_number: int | None
    lesson: BaseLessonSchema
    status: AttendanceStatus = AttendanceStatus.ABSENT
    audience: AudienceSchema
    teachers: list[UserFullNameSchema]

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
