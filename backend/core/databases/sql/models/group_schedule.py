import uuid

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class GroupSchedule(Base):
    __tablename__ = "groups_schedules"
    __table_args__ = (
        UniqueConstraint(
            "group_id",
            "schedule_id",
            name="idx_uniq_subgroup_schedule",
        ),
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "group_numbers.id",
            ondelete="CASCADE",
        )
    )
    schedule_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "schedules.id",
            ondelete="CASCADE",
        )
    )
