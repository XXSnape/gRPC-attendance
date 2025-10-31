import datetime
import uuid
from abc import ABC, abstractmethod

from core.databases.sql.dao.protocols.schedule import (
    ScheduleProtocol,
)
from core.grpc.pb import lesson_service_pb2
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService(ABC):
    dao_class: type[ScheduleProtocol]

    def __init__(self, session: AsyncSession | None = None):
        self._session: AsyncSession | None = session

    async def get_user_lessons_for_month(
        self,
        month: int,
        year: int,
        user_id: uuid.UUID,
    ):
        dates = await self.dao_class(
            self._session
        ).get_user_lessons_for_month(
            month,
            year,
            user_id,
        )
        return lesson_service_pb2.LessonsForMonthResponse(
            dates=[str(date) for date in dates]
        )

    @abstractmethod
    async def get_schedule_by_date(
        self,
        date: datetime.date,
        user_id: uuid.UUID,
    ): ...
