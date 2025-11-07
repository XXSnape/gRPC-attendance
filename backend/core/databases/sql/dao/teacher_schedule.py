import uuid
from datetime import datetime

from core.databases.sql.models import (
    GroupSchedule,
    GroupWithNumber,
    Schedule,
    StudentGroup,
    TeacherSchedule,
)
from sqlalchemy import extract, select
from sqlalchemy.orm import selectinload

from .protocols.schedule import ScheduleProtocol


class TeacherScheduleDAO(ScheduleProtocol):
    model = TeacherSchedule

    async def get_user_lessons_for_month(
        self,
        month: int,
        year: int,
        user_id: uuid.UUID,
    ):
        query = (
            select(Schedule.date.distinct())
            .join(
                TeacherSchedule,
            )
            .where(
                extract("YEAR", Schedule.date) == year,
                extract("MONTH", Schedule.date) == month,
                TeacherSchedule.teacher_id == user_id,
            )
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_schedule_by_date(
        self,
        date: datetime.date,
        user_id: uuid.UUID,
    ):
        query = (
            select(Schedule)
            .join(
                TeacherSchedule,
            )
            .where(
                TeacherSchedule.teacher_id == user_id,
                Schedule.date == date,
            )
            .options(*self.SCHEDULE_OPTIONS)
            .order_by(Schedule.number, Schedule.subgroup_number)
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_lesson_details(
        self,
        user_id: uuid.UUID,
        schedule_id: uuid.UUID,
    ) -> Schedule | None:
        query = (
            select(Schedule)
            .join(TeacherSchedule)
            .where(
                TeacherSchedule.teacher_id == user_id,
                Schedule.id == schedule_id,
            )
            .options(
                *(
                    self.SCHEDULE_OPTIONS
                    + (
                        selectinload(Schedule.groups_with_numbers)
                        .selectinload(
                            GroupWithNumber.students_with_groups
                        )
                        .joinedload(StudentGroup.student),
                    )
                )
            )
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def does_teacher_have_group_in_schedule(
        self,
        teacher_id: uuid.UUID,
        schedule_id: uuid.UUID,
        group_id: uuid.UUID | None,
    ) -> bool:
        query = (
            select(1)
            .join(TeacherSchedule)
            .select_from(Schedule)
            .where(
                TeacherSchedule.teacher_id == teacher_id,
                Schedule.id == schedule_id,
            )
        ).limit(1)
        if group_id is not None:
            query = query.join(
                GroupSchedule,
            ).where(
                GroupSchedule.group_id == group_id,
            )
        result = await self._session.execute(query)
        return result.scalar_one_or_none() is not None
