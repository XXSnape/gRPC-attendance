from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .enums.role import RoleEnum
from .mixins.id_uuid import UUIDIdMixin


class Role(UUIDIdMixin, Base):
    role: Mapped[RoleEnum] = mapped_column(unique=True)
