import uuid

from sqlalchemy import ForeignKey, UniqueConstraint, false
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .enums.form_of_education import FormOfEducationEnum
from .enums.type_of_refund import TypeOfRefundEnum
from .mixins.id_uuid import UUIDIdMixin


class UserGroup(UUIDIdMixin, Base):
    __tablename__ = "users_groups"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "group_id",
            "year_of_admission",
            name="idx_uniq_user_group",
        ),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "groups.id",
            ondelete="CASCADE",
        )
    )
    year_of_admission: Mapped[int]
    form_of_education: Mapped[FormOfEducationEnum]
    type_of_refund: Mapped[TypeOfRefundEnum]
    is_prefect: Mapped[bool] = mapped_column(
        default=False,
        server_default=false(),
    )
