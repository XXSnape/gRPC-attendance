import uuid

from sqlalchemy import UUID, func
from sqlalchemy.ext.asyncio import AsyncAttrs

from core.config import settings
from sqlalchemy import MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)


class Base(AsyncAttrs, DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.
    """

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v7(),
        primary_key=True,
    )

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    number_output_fields = 3

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Возвращает название таблицы по имени модели.
        """
        return f"{cls.__name__.lower()}s"

    def __repr__(self) -> str:
        """
        Возвращает строку с первыми 3 колонками и значениями.
        """
        cols = [
            f"{field}={getattr(self, field)}"
            for field in self.__table__.columns.keys()
            if field != "id" and "_id" not in field
        ][: self.number_output_fields]

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
