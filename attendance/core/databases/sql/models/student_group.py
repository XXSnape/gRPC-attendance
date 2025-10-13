import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
    false,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums.form_of_education import FormOfEducationEnum
from .enums.type_of_refund import TypeOfRefundEnum
from .mixins.id_uuid import UUIDIdMixin


if TYPE_CHECKING:
    from .user import Student
    from .group_number import GroupWithNumber


class StudentGroup(UUIDIdMixin, Base):
    __tablename__ = "students_groups"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "group_id",
            name="idx_uniq_user_group",
        ),
    )

    student_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "students.id",
            ondelete="CASCADE",
        )
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "group_numbers.id",
            ondelete="CASCADE",
        )
    )
    form_of_education: Mapped[FormOfEducationEnum]
    type_of_refund: Mapped[TypeOfRefundEnum]
    is_prefect: Mapped[bool] = mapped_column(
        default=False,
        server_default=false(),
    )
    student: Mapped["Student"] = relationship(
        back_populates="groups",
    )
    group: Mapped["GroupWithNumber"] = relationship(
        back_populates="students",
    )
