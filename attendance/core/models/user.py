import datetime
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .enums.degree import DegreeEnum
from .enums.gender import GenderEnum
from .enums.rank import RankEnum
from .mixins.id_uuid import UUIDIdMixin


class User(UUIDIdMixin, Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped[str]
    password: Mapped[bytes]
    is_active: Mapped[bool]
    email: Mapped[str] = mapped_column(
        unique=True,
    )
    gender: Mapped[GenderEnum]
    date_of_birth: Mapped[datetime.date]

    type: Mapped[str]
    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "user",
    }


class Student(User):
    id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    personal_number: Mapped[str] = mapped_column(
        unique=True,
    )

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }


class Teacher(User):
    id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "departments.id",
            ondelete="CASCADE",
        )
    )
    is_eldest: Mapped[bool]
    rank: Mapped[RankEnum | None]
    degree: Mapped[DegreeEnum | None]

    __mapper_args__ = {
        "polymorphic_identity": "teacher",
    }


class Administrator(User):
    id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    __mapper_args__ = {
        "polymorphic_identity": "administrator",
    }
