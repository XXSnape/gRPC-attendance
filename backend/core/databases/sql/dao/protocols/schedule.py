import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy.orm import joinedload, selectinload

from core.databases.sql.dao.base import BaseDAO
from core.databases.sql.models import (
    Schedule,
    Audience,
    Teacher,
    GroupWithNumber,
    StudentGroup,
)


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
    LESSON_DETAILS_OPTIONS = SCHEDULE_OPTIONS + (
        selectinload(Schedule.groups_with_numbers)
        .selectinload(GroupWithNumber.students_with_groups)
        .joinedload(StudentGroup.student),
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
    ) -> Schedule | None:
        pass
