import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, null
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums.type_of_lesson import TypeOfLessonEnum
from .mixins.id_uuid import UUIDIdMixin

if TYPE_CHECKING:
    from .audience import Audience
    from .group_number import GroupWithNumber
    from .lesson import Lesson
    from .schedule_exceptions import ScheduleException
    from .user import Student, Teacher


class Schedule(UUIDIdMixin, Base):
    __table_args__ = (
        CheckConstraint(
            "number >= 1 AND number <= 6", name="idx_number"
        ),
        CheckConstraint(
            "subgroup_number IS NULL or "
            "(subgroup_number >= 1 AND subgroup_number <= 2)",
            name="idx_subgroup_number",
        ),
    )

    type_of_lesson: Mapped[TypeOfLessonEnum]
    date: Mapped[datetime.date]
    number: Mapped[int]
    subgroup_number: Mapped[int | None] = mapped_column(
        default=None,
        server_default=null(),
    )
    type: Mapped[str]

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "lessons.id",
            ondelete="CASCADE",
        )
    )
    audience_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "audiences.id",
            ondelete="CASCADE",
        )
    )

    lesson: Mapped["Lesson"] = relationship(
        back_populates="schedules",
    )
    audience: Mapped["Audience"] = relationship(
        back_populates="schedules",
    )
    exceptions: Mapped[list["ScheduleException"]] = relationship(
        back_populates="schedule",
    )
    teachers: Mapped[list["Teacher"]] = relationship(
        secondary="teachers_schedules",
        back_populates="schedules",
    )

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "schedule",
    }


class GroupSchedule(Schedule):
    __tablename__ = "groups_schedules"
    id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "schedules.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "group_numbers.id",
            ondelete="CASCADE",
        )
    )

    group: Mapped["GroupWithNumber"] = relationship(
        back_populates="schedules",
    )

    __mapper_args__ = {
        "polymorphic_identity": "groups_schedule",
    }


class PersonalSchedule(Schedule):
    __tablename__ = "personals_schedules"
    id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "schedules.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )
    student: Mapped["Student"] = relationship(
        back_populates="schedules",
    )
    __mapper_args__ = {
        "polymorphic_identity": "personals_schedule",
    }
