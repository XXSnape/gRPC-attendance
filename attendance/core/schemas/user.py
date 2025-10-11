import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr

from core.databases.sql.models.enums.gender import GenderEnum


class BaseUserSchema(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    password: str
    is_active: bool
    email: EmailStr
    gender: GenderEnum
    type: Literal[
        "student",
        "teacher",
        "administrator",
    ]
    date_of_birth: datetime.date


class HashedPasswordUserSchema(BaseUserSchema):
    password: bytes
