from .mixins.id_uuid import UUIDIdMixin
from sqlalchemy.orm import Mapped

from .base import Base
from .mixins.id_uuid import UUIDIdMixin


class Course(Base):
    year_of_admission: Mapped[int]
