import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.id_uuid import UUIDIdMixin

if TYPE_CHECKING:
    from .schedule import GroupSchedule
    from .student_group import StudentGroup
    from .group import Group


class GroupWithNumber(UUIDIdMixin, Base):
    __tablename__ = "group_numbers"
    __table_args__ = (
        UniqueConstraint(
            "group_id",
            "number",
            "year_of_admission",
            name="idx_uniq_number_group",
        ),
        CheckConstraint("number >= 1", name="idx_group_number"),
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "groups.id",
            ondelete="CASCADE",
        )
    )
    number: Mapped[int]
    year_of_admission: Mapped[int]
    schedules: Mapped[list["GroupSchedule"]] = relationship(
        back_populates="group",
    )
    students: Mapped[list["StudentGroup"]] = relationship(
        back_populates="group",
    )
    group: Mapped["Group"] = relationship(
        back_populates="numbers",
    )
