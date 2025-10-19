import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums.type_of_lesson import TypeOfLessonEnum

if TYPE_CHECKING:
    from .audience import Audience
    from .group_schedule import GroupSchedule
    from .lesson import Lesson
    from .schedule_exceptions import ScheduleException
    from .user import Teacher


class Schedule(Base):
    __table_args__ = (
        CheckConstraint(
            "number >= 1 AND number <= 6", name="idx_number"
        ),
        UniqueConstraint(
            "type_of_lesson",
            "date",
            "number",
            "lesson_id",
            "audience_id",
            name="idx_uniq_schedule",
        ),
    )

    type_of_lesson: Mapped[TypeOfLessonEnum]
    date: Mapped[datetime.date]
    number: Mapped[int]

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
    groups_with_subgroups: Mapped[list["GroupSchedule"]] = (
        relationship(
            back_populates="schedule",
        )
    )
