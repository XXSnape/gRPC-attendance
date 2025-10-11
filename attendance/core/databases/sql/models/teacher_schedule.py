import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.id_uuid import UUIDIdMixin


class TeacherSchedule(UUIDIdMixin, Base):
    __tablename__ = "teachers_schedules"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
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

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )
