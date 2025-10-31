import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .schedule import Schedule


class TeacherSchedule(Base):
    __tablename__ = "teachers_schedules"
    __table_args__ = (
        UniqueConstraint(
            "teacher_id",
            "schedule_id",
            name="idx_uniq_teacher_schedule",
        ),
    )

    schedule_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "schedules.id",
            ondelete="CASCADE",
        )
    )

    teacher_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "teachers.id",
            ondelete="CASCADE",
        )
    )
