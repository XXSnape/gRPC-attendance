import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.id_uuid import UUIDIdMixin


class TeacherDepartment(UUIDIdMixin, Base):
    __tablename__ = "teachers_departments"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "department_id",
            name="idx_uniq_teacher_department",
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "departments.id",
            ondelete="CASCADE",
        )
    )
