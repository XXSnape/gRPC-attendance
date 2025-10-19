import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums.level import LevelEnum

if TYPE_CHECKING:
    from .department import Department
    from .group_number import GroupWithNumber
    from .specialization import Specialization


class Group(Base):
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
    department: Mapped["Department"] = relationship(
        back_populates="groups",
    )
    specialization: Mapped["Specialization"] = relationship(
        back_populates="groups",
    )
    numbers: Mapped[list["GroupWithNumber"]] = relationship(
        back_populates="group",
    )
