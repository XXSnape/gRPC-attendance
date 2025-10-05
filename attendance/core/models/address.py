from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.id_uuid import UUIDIdMixin


class Address(UUIDIdMixin, Base):
    __tablename__ = "addresses"
    name: Mapped[str] = mapped_column(unique=True)
