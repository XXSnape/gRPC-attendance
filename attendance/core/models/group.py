import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .enums.group import GroupEnum
from .mixins.id_uuid import UUIDIdMixin


class Group(UUIDIdMixin, Base):
    __table_args__ = (
        UniqueConstraint(
            "name",
            "type",
            "year_of_admission",
            "specialization_id",
            name="idx_uniq_group",
        ),
    )
    name: Mapped[str] = mapped_column(unique=True)
    type: Mapped[GroupEnum]
    year_of_admission: Mapped[int]
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
