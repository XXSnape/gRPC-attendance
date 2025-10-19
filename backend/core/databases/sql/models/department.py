from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .lesson import Lesson


if TYPE_CHECKING:
    from .group import Group
    from .user import Teacher


class Department(Base):
    name: Mapped[str] = mapped_column(
        unique=True,
    )
    groups: Mapped[list["Group"]] = relationship(
        back_populates="department",
    )
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="department",
    )
    teachers: Mapped[list["Teacher"]] = relationship(
        back_populates="department",
    )
