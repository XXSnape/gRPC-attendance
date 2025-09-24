import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins.id_uuid import UUIDIdMixin


class UserRole(UUIDIdMixin, Base):
    __tablename__ = "users_roles"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "role_id",
            name="idx_uniq_user_role",
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "roles.id",
            ondelete="CASCADE",
        ),
    )
