import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .enums.level import LevelEnum
from .mixins.id_uuid import UUIDIdMixin


class Group(UUIDIdMixin, Base):
    __table_args__ = (
        UniqueConstraint(
            "level",
            "department_id",
            "specialization_id",
            name="idx_uniq_group",
        ),
    )
    name: Mapped[str] = mapped_column(unique=True)
    level: Mapped[LevelEnum]
    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "departments.id",
            ondelete="CASCADE",
        )
    )
    specialization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "specializations.id",
            ondelete="CASCADE",
        ),
    )
