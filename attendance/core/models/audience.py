import uuid

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.id_uuid import UUIDIdMixin


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
