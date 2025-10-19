from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .audience import Audience


class Address(Base):
    __tablename__ = "addresses"
    name: Mapped[str] = mapped_column(unique=True)
    audiences: Mapped[list["Audience"]] = relationship(
        back_populates="address",
    )
