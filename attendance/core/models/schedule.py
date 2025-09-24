import datetime
import uuid

from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.id_uuid import UUIDIdMixin


class Schedule(UUIDIdMixin, Base):
    __table_args__ = (
        CheckConstraint("number >= 1 AND number <= 6", name="idx_number"),
        UniqueConstraint(
            "group_id",
            "lesson_id",
            "audience_id",
            "teacher_id",
            "number",
            "date",
            name="idx_uniq_group_lesson",
        ),
    )

    group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "groups.id",
            ondelete="CASCADE",
        )
    )
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
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )
    date: Mapped[datetime.date]
    number: Mapped[int]
