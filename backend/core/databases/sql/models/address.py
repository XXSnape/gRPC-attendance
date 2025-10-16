from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.id_uuid import UUIDIdMixin

if TYPE_CHECKING:
    from .audience import Audience


class Address(UUIDIdMixin, Base):
    __tablename__ = "addresses"
    name: Mapped[str] = mapped_column(unique=True)
    audiences: Mapped[list["Audience"]] = relationship(
        back_populates="address",
    )
