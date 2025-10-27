import datetime
import uuid
from typing import Literal

from core.databases.sql.models.enums.gender import GenderEnum
from pydantic import EmailStr
from services.base import BaseService

from .attendance import AttendanceSchema
from .common import BaseSchema, IdSchema


class UserFullNameSchema(BaseSchema):
    full_name: str
    decryption_of_full_name: str


class UserAttendanceSchema(
    UserFullNameSchema,
):
    student_id: uuid.UUID
    personal_number: str
    attendance: AttendanceSchema = AttendanceSchema()
    is_prefect: bool = False


class UserEmailSchema(BaseSchema):
    email: EmailStr


class UserInSchema(UserEmailSchema):
    password: str


class BaseUserSchema(UserInSchema):
    first_name: str
    last_name: str
    patronymic: str
    is_active: bool
    gender: GenderEnum
    type: Literal[
        "student",
        "teacher",
        "administrator",
    ]
    date_of_birth: datetime.date


class HashedPasswordUserSchema(BaseUserSchema):
    password: bytes


class UserDataSchema(IdSchema):
    type: Literal[
        "student",
        "teacher",
        "administrator",
    ]
    full_name: str | None = None

    def get_service_by_role(self) -> type[BaseService]:
        from services.student import StudentService
        from services.teacher import TeacherService

        match self.type:
            case "student":
                return StudentService
            case "teacher":
                return TeacherService
            case _:
                return StudentService
