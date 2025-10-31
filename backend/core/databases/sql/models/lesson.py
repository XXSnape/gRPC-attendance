import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, true, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .department import Department
    from .schedule import Schedule


class Lesson(Base):
    __table_args__ = (
        UniqueConstraint(
            "name",
            "department_id",
            name="idx_uniq_lesson_department",
        ),
    )
    name: Mapped[str] = mapped_column(unique=True)
    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "departments.id",
            ondelete="CASCADE",
        )
    )
    department: Mapped["Department"] = relationship(
        back_populates="lessons",
    )
    schedules: Mapped[list["Schedule"]] = relationship(
        back_populates="lesson",
    )

    type: Mapped[str]
    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "lesson",
    }


class LessonType(Base):
    __tablename__ = "lessons_types"
    id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "lessons.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    kind: Mapped[str]

    __mapper_args__ = {"polymorphic_identity": "lesson_type"}
