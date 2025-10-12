import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
    false,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums.form_of_education import FormOfEducationEnum
from .enums.type_of_refund import TypeOfRefundEnum
from .mixins.id_uuid import UUIDIdMixin


if TYPE_CHECKING:
    from .group import Group
    from .user import Student


class StudentGroup(UUIDIdMixin, Base):
    __tablename__ = "students_groups"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "group_id",
            "year_of_admission",
            name="idx_uniq_user_group",
        ),
        CheckConstraint("number >= 1", name="idx_group_number"),
    )

    student_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "students.id",
            ondelete="CASCADE",
        )
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "groups.id",
            ondelete="CASCADE",
        )
    )
    year_of_admission: Mapped[int]
    form_of_education: Mapped[FormOfEducationEnum]
    number: Mapped[int]
    type_of_refund: Mapped[TypeOfRefundEnum]
    is_prefect: Mapped[bool] = mapped_column(
        default=False,
        server_default=false(),
    )
    student: Mapped["Student"] = relationship(
        back_populates="groups",
    )
    group: Mapped["Group"] = relationship(
        back_populates="students",
    )
