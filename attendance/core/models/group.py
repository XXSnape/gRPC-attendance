from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .enums.groups import GroupEnum
from .mixins.id_uuid import UUIDIdMixin


class Group(UUIDIdMixin, Base):
    name: Mapped[str] = mapped_column(unique=True)
    type: Mapped[GroupEnum]
