import datetime
from typing import Literal

from pydantic import EmailStr, ConfigDict

from core.databases.sql.models.enums.gender import GenderEnum
from .common import BaseSchema


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


class UserData(BaseSchema):
    type: Literal[
        "student",
        "teacher",
        "administrator",
    ]
    full_name: str
    model_config = ConfigDict(from_attributes=True)


class UserSignedUpSchema(BaseSchema):
    token: str
    user: UserData
