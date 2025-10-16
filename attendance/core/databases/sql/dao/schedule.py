from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from .base import BaseDAO
from core.databases.sql.models import (
    GroupSchedule,
    StudentGroup,
    Audience,
    Teacher,
)
import uuid
import datetime


class GroupScheduleDAO(BaseDAO):
    model = GroupSchedule

    async def get_user_lessons(
        self,
        date: str,
        user_id: uuid.UUID,
    ):
        date = datetime.date.fromisoformat(date)
        group_id_subq = (
            select(StudentGroup.group_id)
            .where(StudentGroup.student_id == user_id)
            .scalar_subquery()
        )
        query = (
            select(GroupSchedule)
            .where(
                GroupSchedule.date == date,
                GroupSchedule.group_id == group_id_subq,
            )
            .options(
                joinedload(GroupSchedule.lesson),
                joinedload(
                    GroupSchedule.audience,
                ).joinedload(Audience.address),
                selectinload(GroupSchedule.teachers).load_only(
                    Teacher.first_name,
                    Teacher.last_name,
                    Teacher.patronymic,
                ),
            )
        )
        result = await self._session.execute(query)
        return result.scalars().all()
