from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.id_uuid import UUIDIdMixin


class Specialization(UUIDIdMixin, Base):
    name: Mapped[str] = mapped_column(
        unique=True,
    )
    code: Mapped[str] = mapped_column(String(20), unique=True)
