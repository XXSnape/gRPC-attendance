from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from .base import BaseDAO
from core.databases.sql.models import GroupSchedule, StudentGroup
import uuid
import datetime


class GroupScheduleDAO(BaseDAO):
    model = GroupSchedule

    async def get_user_lessons(
        self,
        date: str,
        user_id: uuid.UUID,
    ):
        # user_id = uuid.UUID(user_id)
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
            .options(joinedload(GroupSchedule.lesson))
        )
        print("query", query)
        result = await self._session.execute(query)
        return result.scalars().all()
