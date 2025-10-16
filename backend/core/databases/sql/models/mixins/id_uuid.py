import uuid

from sqlalchemy import UUID, func
from sqlalchemy.orm import Mapped, mapped_column


class UUIDIdMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v7(),
        primary_key=True,
    )
