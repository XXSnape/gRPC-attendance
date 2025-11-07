import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


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
