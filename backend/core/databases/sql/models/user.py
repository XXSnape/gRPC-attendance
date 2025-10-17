import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums.degree import DegreeEnum
from .enums.gender import GenderEnum
from .enums.rank import RankEnum
from .mixins.id_uuid import UUIDIdMixin

if TYPE_CHECKING:
    from .department import Department
    from .schedule import PersonalSchedule, Schedule
    from .schedule_exceptions import ScheduleException
    from .student_group import StudentGroup


class User(UUIDIdMixin, Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped[str]
    password: Mapped[bytes]
    is_active: Mapped[bool]
    email: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )
    gender: Mapped[GenderEnum]
    date_of_birth: Mapped[datetime.date]

    type: Mapped[str]
    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "user",
    }

    @hybrid_property
    def full_name(self):
        return (
            f"{self.last_name.title()}"
            f" {self.first_name[0].title()}. {self.patronymic[0].title()}."
        )

    @hybrid_property
    def decryption_of_full_name(self):
        return (
            f"{self.last_name} {self.first_name} {self.patronymic}"
        )

    def __str__(self):
        return self.full_name


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
    schedules: Mapped[list["PersonalSchedule"]] = relationship(
        back_populates="student",
    )
    schedule_exceptions: Mapped[list["ScheduleException"]] = (
        relationship(
            back_populates="student",
        )
    )
    groups: Mapped[list["StudentGroup"]] = relationship(
        back_populates="student",
        foreign_keys="StudentGroup.student_id",
        primaryjoin="Student.id == StudentGroup.student_id",
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
    department: Mapped["Department"] = relationship(
        back_populates="teachers",
    )
    schedules: Mapped[list["Schedule"]] = relationship(
        secondary="teachers_schedules",
        back_populates="teachers",
    )

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
