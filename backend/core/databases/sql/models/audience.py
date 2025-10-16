import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.id_uuid import UUIDIdMixin

if TYPE_CHECKING:
    from .address import Address
    from .schedule import Schedule


class Audience(UUIDIdMixin, Base):
    __table_args__ = (
        UniqueConstraint(
            "name",
            "address_id",
            name="idx_uniq_name_address",
        ),
    )
    name: Mapped[str]
    address_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "addresses.id",
            ondelete="CASCADE",
        )
    )
    schedules: Mapped[list["Schedule"]] = relationship(
        back_populates="audience",
    )
    address: Mapped["Address"] = relationship(
        back_populates="audiences",
    )
