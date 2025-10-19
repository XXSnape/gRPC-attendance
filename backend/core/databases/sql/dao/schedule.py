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
    base_options = (
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
            .options(*self.base_options)
        )
        # base_query = self.generate_base_schedule_query(user_id)
        # query = base_query.where(GroupSchedule.date == date)
        # group_id_subq = (
        #     select(StudentGroup.group_id)
        #     .where(
        #         StudentGroup.student_id == user_id,
        #     )
        #     .scalar_subquery()
        # )
        # query = (
        #     select(GroupSchedule)
        #     .where(
        #         GroupSchedule.group_id == group_id_subq,
        #         GroupSchedule.date == date,
        #     )
        #     .options(
        #         joinedload(GroupSchedule.lesson),
        #         joinedload(
        #             GroupSchedule.audience,
        #         ).joinedload(Audience.address),
        #         selectinload(GroupSchedule.teachers).load_only(
        #             Teacher.first_name,
        #             Teacher.last_name,
        #             Teacher.patronymic,
        #         ),
        #     )
        # )
        # if date:
        #     date = datetime.date.fromisoformat(date)
        #     query = query.where(GroupSchedule.date == date)
        # if lesson_id:
        #     query = query.where(
        #         GroupSchedule.lesson_id == uuid.UUID(lesson_id)
        #     ).options(
        #         joinedload(GroupSchedule.group).joinedload(
        #             GroupWithNumber.group
        #         ),
        #         joinedload(GroupSchedule.group)
        #         .selectinload(GroupWithNumber.students_with_groups)
        #         .joinedload(StudentGroup.student),
        #     )
        #     result = await self._session.execute(query)
        #     return result.scalars().one_or_none()
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
        ).distinct()
        exist_result = await self._session.execute(exists_query)
        if exist_result.scalar_one_or_none() is None:
            return None
        # base_options = (
        #     joinedload(GroupSchedule.schedule).joinedload(
        #         Schedule.lesson
        #     ),
        #     joinedload(GroupSchedule.schedule)
        #     .joinedload(Schedule.audience)
        #     .joinedload(Audience.address),
        #     joinedload(GroupSchedule.schedule)
        #     .selectinload(Schedule.teachers)
        #     .load_only(
        #         Teacher.first_name,
        #         Teacher.last_name,
        #         Teacher.patronymic,
        #     ),
        # )
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
        # query = (
        #     select(GroupSchedule)
        #     .join(Schedule)
        #     .where(Schedule.id == uuid.UUID(schedule_id))
        #     .options(*self.base_options)
        #     .options(
        #         joinedload(
        #             GroupSchedule.group_with_number
        #         ).joinedload(GroupWithNumber.group),
        #         joinedload(GroupSchedule.group_with_number)
        #         .selectinload(GroupWithNumber.students_with_groups)
        #         .joinedload(StudentGroup.student),
        #     )
        # )
        result = await self._session.execute(query)
        return result.all()
        # return await self._session.scalars(query)

        # subq = (
        #     select(GroupSchedule)
        #     .where(
        #         GroupSchedule.group_id == group_id_subq,
        #         GroupSchedule.lesson_id == uuid.UUID(lesson_id),
        #     ).exists()

        # query = select(GroupSchedule)

    # async def get_user_lessons(
    #     self,
    #     date: str | None,
    #     user_id: uuid.UUID,
    #     lesson_id: str | None = None,
    # ):
    #     group_id_subq = (
    #         select(StudentGroup.group_id)
    #         .where(StudentGroup.student_id == user_id)
    #         .scalar_subquery()
    #     )
    #     query = (
    #         select(GroupSchedule)
    #         .where(
    #             GroupSchedule.group_id == group_id_subq,
    #         )
    #         .options(
    #             joinedload(GroupSchedule.lesson),
    #             joinedload(
    #                 GroupSchedule.audience,
    #             ).joinedload(Audience.address),
    #             selectinload(GroupSchedule.teachers).load_only(
    #                 Teacher.first_name,
    #                 Teacher.last_name,
    #                 Teacher.patronymic,
    #             ),
    #         )
    #     )
    #     if date:
    #         date = datetime.date.fromisoformat(date)
    #         query = query.where(GroupSchedule.date == date)
    #     if lesson_id:
    #         query = query.where(
    #             GroupSchedule.lesson_id == uuid.UUID(lesson_id)
    #         ).options(
    #             joinedload(GroupSchedule.group).joinedload(
    #                 GroupWithNumber.group
    #             ),
    #             joinedload(GroupSchedule.group)
    #             .selectinload(GroupWithNumber.students_with_groups)
    #             .joinedload(StudentGroup.student),
    #         )
    #         result = await self._session.execute(query)
    #         return result.scalars().one_or_none()
    #     result = await self._session.execute(query)
    #     return result.scalars().all()

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
