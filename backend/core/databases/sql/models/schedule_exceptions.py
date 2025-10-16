import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.id_uuid import UUIDIdMixin

if TYPE_CHECKING:
    from .schedule import Schedule
    from .user import Student


class ScheduleException(UUIDIdMixin, Base):
    __tablename__ = "schedule_exceptions"

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
    schedule: Mapped["Schedule"] = relationship(
        back_populates="exceptions"
    )
    student: Mapped["Student"] = relationship(
        back_populates="schedule_exceptions"
    )
