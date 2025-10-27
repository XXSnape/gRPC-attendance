import datetime
import uuid

from core.databases.sql.models import (
    Audience,
    GroupSchedule,
    GroupWithNumber,
    Schedule,
    StudentGroup,
    Teacher,
)
from sqlalchemy import extract, select
from sqlalchemy.orm import (
    joinedload,
    selectinload,
)

from .protocols.schedule import ScheduleProtocol


class GroupScheduleDAO(ScheduleProtocol):
    model = GroupSchedule

    def get_subquery_group_id_by_user(self, user_id: uuid.UUID):
        group_id_subq = (
            select(StudentGroup.group_id)
            .where(
                StudentGroup.student_id == user_id,
            )
            .scalar_subquery()
        )
        return group_id_subq

    async def get_user_lessons(
        self,
        date: str,
        user_id: uuid.UUID,
    ):
        date = datetime.date.fromisoformat(date)
        group_id_subq = self.get_subquery_group_id_by_user(user_id)
        query = (
            select(GroupSchedule)
            .join(Schedule)
            .where(
                GroupSchedule.group_id == group_id_subq,
                Schedule.date == date,
            )
            .options(
                joinedload(GroupSchedule.schedule).joinedload(
                    Schedule.lesson
                ),
                joinedload(GroupSchedule.schedule)
                .joinedload(Schedule.audience)
                .joinedload(Audience.address),
                joinedload(GroupSchedule.schedule)
                .selectinload(Schedule.teachers)
                .load_only(
                    Teacher.first_name,
                    Teacher.last_name,
                    Teacher.patronymic,
                ),
            )
        )
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_lesson_details(
        self,
        user_id: uuid.UUID,
        schedule_id: str,
    ):
        group_id_subq = self.get_subquery_group_id_by_user(user_id)
        exists_query = (
            select(1)
            .select_from(GroupSchedule)
            .join(Schedule)
            .where(
                GroupSchedule.group_id == group_id_subq,
            )
            .limit(1)
        )
        exist_result = await self._session.execute(exists_query)
        if exist_result.scalar_one_or_none() is None:
            return None
        query = (
            select(Schedule, group_id_subq)
            .where(Schedule.id == uuid.UUID(schedule_id))
            .options(
                joinedload(Schedule.audience).joinedload(
                    Audience.address
                ),
                joinedload(Schedule.lesson),
                selectinload(Schedule.teachers).load_only(
                    Teacher.first_name,
                    Teacher.last_name,
                    Teacher.patronymic,
                ),
                selectinload(Schedule.groups_with_subgroups)
                .joinedload(GroupSchedule.group_with_number)
                .joinedload(GroupWithNumber.group),
                selectinload(Schedule.groups_with_subgroups)
                .joinedload(GroupSchedule.group_with_number)
                .selectinload(GroupWithNumber.students_with_groups)
                .joinedload(StudentGroup.student),
            )
        )
        result = await self._session.execute(query)
        return result.first()

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
        query = (
            select(Schedule.date.distinct())
            .join(
                GroupSchedule,
            )
            .where(
                extract("YEAR", Schedule.date) == year,
                extract("MONTH", Schedule.date) == month,
                GroupSchedule.group_id == group_id_subq,
            )
        )
        result = await self._session.execute(query)
        return result.scalars().all()

    async def check_is_prefect_in_group(
        self, group_id: str, user_id: uuid.UUID
    ) -> bool:

        query = (
            select(StudentGroup).where(
                StudentGroup.group_id == uuid.UUID(group_id),
                StudentGroup.student_id == user_id,
                StudentGroup.is_prefect.is_(True),
            )
        ).limit(1)
        result = await self._session.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_students_of_group(
        self,
        schedule_id: str,
        group_id: str,
    ) -> GroupSchedule | None:

        query = (
            select(GroupSchedule)
            .where(
                GroupSchedule.group_id == uuid.UUID(group_id),
                GroupSchedule.schedule_id == uuid.UUID(schedule_id),
            )
            .options(
                joinedload(
                    GroupSchedule.group_with_number
                ).selectinload(GroupWithNumber.students_with_groups)
            )
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()
