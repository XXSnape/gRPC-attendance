from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.id_uuid import UUIDIdMixin


class Specialization(UUIDIdMixin, Base):
    name: Mapped[str] = mapped_column(
        unique=True,
    )
