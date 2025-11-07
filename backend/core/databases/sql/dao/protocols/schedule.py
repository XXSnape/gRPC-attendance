import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from core.databases.sql.dao.base import BaseDAO
from core.databases.sql.models import (
    Audience,
    GroupWithNumber,
    Schedule,
    Teacher,
)
from sqlalchemy.orm import joinedload, selectinload


class ScheduleProtocol(BaseDAO, ABC):
    SCHEDULE_OPTIONS = (
        joinedload(Schedule.lesson),
        selectinload(Schedule.audiences).joinedload(
            Audience.address
        ),
        selectinload(Schedule.teachers).load_only(
            Teacher.first_name,
            Teacher.last_name,
            Teacher.patronymic,
        ),
        selectinload(Schedule.groups_with_numbers).joinedload(
            GroupWithNumber.group
        ),
    )

    @abstractmethod
    async def get_user_lessons_for_month(
        self,
        month: int,
        year: int,
        user_id: uuid.UUID,
    ) -> list[datetime.date]: ...

    @abstractmethod
    async def get_schedule_by_date(
        self,
        date: datetime.date,
        user_id: uuid.UUID,
    ) -> list[Schedule]: ...

    @abstractmethod
    async def get_lesson_details(
        self,
        user_id: uuid.UUID,
        schedule_id: uuid.UUID,
    ) -> Schedule | None: ...
