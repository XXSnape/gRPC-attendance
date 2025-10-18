import uuid
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.id_uuid import UUIDIdMixin

if TYPE_CHECKING:
    from .group import Group
    from .schedule import GroupSchedule
    from .student_group import StudentGroup


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
    students_with_groups: Mapped[list["StudentGroup"]] = (
        relationship(
            back_populates="group_with_number",
        )
    )
    group: Mapped["Group"] = relationship(
        back_populates="numbers",
    )

    @hybrid_property
    def complete_name(self):
        return (
            f"{self.group.name.upper()}-{self.number}-"
            f"({str(self.year_of_admission)[-2:]})"
        )
