import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AudienceSchedule(Base):
    __tablename__ = "audiences_schedules"

    __table_args__ = (
        UniqueConstraint(
            "audience_id",
            "schedule_id",
            name="idx_uniq_audience_schedule",
        ),
    )

    audience_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "audiences.id",
            ondelete="CASCADE",
        )
    )
    schedule_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "schedules.id",
            ondelete="CASCADE",
        )
    )
