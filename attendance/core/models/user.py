from sqlalchemy.orm import Mapped

from .base import Base
from .mixins.id_uuid import UUIDIdMixin


class User(UUIDIdMixin, Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped[str]
    password: Mapped[bytes]
    is_active: Mapped[bool]
