import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    UniqueConstraint,
    null,
    true,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums.type_of_lesson import TypeOfLessonEnum

if TYPE_CHECKING:
    from .audience import Audience
    from .group_number import GroupWithNumber
    from .lesson import Lesson
    from .schedule_exceptions import ScheduleException
    from .user import Teacher


class Schedule(Base):
    __table_args__ = (
        CheckConstraint(
            "number >= 1 AND number <= 6", name="idx_number"
        ),
        CheckConstraint(
            "subgroup_number IS NULL or "
            "(subgroup_number >= 1 AND subgroup_number <= 2)",
            name="idx_subgroup_number",
        ),
        UniqueConstraint(
            "type_of_lesson",
            "date",
            "number",
            "lesson_id",
            "subgroup_number",
            name="idx_uniq_schedule",
        ),
    )

    type_of_lesson: Mapped[TypeOfLessonEnum]
    date: Mapped[datetime.date]
    number: Mapped[int]
    subgroup_number: Mapped[int | None] = mapped_column(
        default=None,
        server_default=null(),
    )
    is_standardized: Mapped[bool] = mapped_column(
        default=True,
        server_default=true(),
    )
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "lessons.id",
            ondelete="CASCADE",
        )
    )

    lesson: Mapped["Lesson"] = relationship(
        back_populates="schedules",
    )
    audiences: Mapped[list["Audience"]] = relationship(
        back_populates="schedules",
        secondary="audiences_schedules",
    )
    exceptions: Mapped[list["ScheduleException"]] = relationship(
        back_populates="schedule",
    )
    teachers: Mapped[list["Teacher"]] = relationship(
        secondary="teachers_schedules",
        back_populates="schedules",
    )
    groups_with_numbers: Mapped[list["GroupWithNumber"]] = (
        relationship(
            secondary="groups_schedules",
            back_populates="schedules",
        )
    )

    @hybrid_property
    def group_names(self):
        return [
            gwn.complete_name for gwn in self.groups_with_numbers
        ]
