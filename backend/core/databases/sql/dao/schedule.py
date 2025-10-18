import datetime
import uuid

from core.databases.sql.models import (
    Audience,
    GroupSchedule,
    StudentGroup,
    Teacher,
    GroupWithNumber,
    Schedule,
)
from sqlalchemy import select, func
from sqlalchemy.orm import (
    joinedload,
    selectinload,
    with_polymorphic,
)

from .base import BaseDAO
from sqlalchemy import extract


class GroupScheduleDAO(BaseDAO):
    model = GroupSchedule

    async def get_user_lessons(
        self,
        date: str | None,
        user_id: uuid.UUID,
        lesson_id: str | None = None,
    ):
        group_id_subq = (
            select(StudentGroup.group_id)
            .where(StudentGroup.student_id == user_id)
            .scalar_subquery()
        )
        query = (
            select(GroupSchedule)
            .where(
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
        if date:
            date = datetime.date.fromisoformat(date)
            query = query.where(GroupSchedule.date == date)
        if lesson_id:
            query = query.where(
                GroupSchedule.lesson_id == uuid.UUID(lesson_id)
            ).options(
                joinedload(GroupSchedule.group).joinedload(
                    GroupWithNumber.group
                )
            )
            result = await self._session.execute(query)
            return result.scalars().one_or_none()
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_user_lessons_for_month(
        self,
        month: int,
        year: int,
        user_id: uuid.UUID,
    ):
        group_id_subq = (
            select(StudentGroup.group_id)
            .where(StudentGroup.student_id == user_id)
            .scalar_subquery()
        )
        query = select(GroupSchedule.date.distinct()).where(
            extract("YEAR", GroupSchedule.date) == year,
            extract("MONTH", GroupSchedule.date) == month,
            GroupSchedule.group_id == group_id_subq,
        )
        result = await self._session.execute(query)
        return result.scalars().all()

    async def check_group_has_lesson(
        self, lesson_id: str, group_id: uuid.UUID
    ) -> bool:

        schedule_poly = with_polymorphic(Schedule, [GroupSchedule])

        query = (
            select(func.count())
            .select_from(schedule_poly)
            .where(
                schedule_poly.lesson_id == uuid.UUID(lesson_id),
                schedule_poly.GroupSchedule.group_id == group_id,
            )
        )
        result = await self._session.execute(query)
        return result.scalar() > 0
