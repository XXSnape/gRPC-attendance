import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .group_number import GroupWithNumber
    from .schedule import Schedule


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

    schedule: Mapped["Schedule"] = relationship(
        back_populates="groups_with_subgroups",
    )
    group_with_number: Mapped["GroupWithNumber"] = relationship(
        back_populates="groups_with_subgroups",
    )
