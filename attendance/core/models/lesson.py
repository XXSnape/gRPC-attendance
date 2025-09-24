from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.id_uuid import UUIDIdMixin
import uuid


class Lesson(UUIDIdMixin, Base):
    __table_args__ = (
        UniqueConstraint(
            "name",
            "department_id",
            name="idx_uniq_name_department_id",
        ),
    )
    name: Mapped[str] = mapped_column(unique=True)
    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "departments.id",
            ondelete="CASCADE",
        )
    )
