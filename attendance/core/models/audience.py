from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped

from .base import Base
from .enums.address import AddressEnum
from .mixins.id_uuid import UUIDIdMixin


class Audience(UUIDIdMixin, Base):
    __table_args__ = (
        UniqueConstraint(
            "name",
            "address",
            name="idx_uniq_name_address",
        ),
    )
    name: Mapped[str]
    address: Mapped[AddressEnum]
