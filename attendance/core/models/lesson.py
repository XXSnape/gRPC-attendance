from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.id_uuid import UUIDIdMixin
import uuid


class Lesson(UUIDIdMixin, Base):
    name: Mapped[str] = mapped_column(unique=True)
    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "departments.id",
            ondelete="CASCADE",
        )
    )
    on_schedule: Mapped[bool] = mapped_column(default=True, server_default="1")
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
