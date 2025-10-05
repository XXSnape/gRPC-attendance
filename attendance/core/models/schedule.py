import datetime
import uuid

from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.id_uuid import UUIDIdMixin


class Schedule(UUIDIdMixin, Base):
    __table_args__ = (
        CheckConstraint("number >= 1 AND number <= 6", name="idx_number"),
        CheckConstraint(
            "subgroup_number IS NULL or "
            "(subgroup_number >= 1 AND subgroup_number <= 2)",
            name="idx_subgroup_number",
        ),
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
    date: Mapped[datetime.date]
    number: Mapped[int]
    subgroup_number: Mapped[int | None] = mapped_column(
        default=None,
        server_default=text("NULL"),
    )
    type: Mapped[str]
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
            "groups.id",
            ondelete="CASCADE",
        )
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
    __mapper_args__ = {
        "polymorphic_identity": "personals_schedule",
    }
