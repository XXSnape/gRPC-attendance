import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from core.databases.sql.dao.base import BaseDAO


class ScheduleProtocol(BaseDAO, ABC):
    @abstractmethod
    async def get_user_lessons_for_month(
        self,
        month: int,
        year: int,
        user_id: uuid.UUID,
    ) -> list[datetime.date]: ...
