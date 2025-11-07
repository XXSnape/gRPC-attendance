import datetime
import uuid

import grpc

from core.databases.no_sql.documents import Visit
from core.databases.sql.dao.group_schedule import GroupScheduleDAO
from core.databases.sql.dao.teacher_schedule import (
    TeacherScheduleDAO,
)
from core.enums.status import AttendanceStatus
from core.grpc.pb import lesson_service_pb2, lesson_pb2
from core.schemas.lesson import (
    TotalAttendance,
    BaseScheduleSchema,
    FullScheduleDataSchema,
)

from .base import BaseService


class TeacherService(BaseService):
    dao_class = TeacherScheduleDAO
    can_t_view_lesson_details = (
        "Запишитесь на это занятие, чтобы просмотреть детали."
    )

    async def get_schedule_by_date(
        self,
        date: datetime.date,
        user_id: uuid.UUID,
    ):
        dao_obj = self.dao_class(self._session)
        schedules = await dao_obj.get_schedule_by_date(
            date=date,
            user_id=user_id,
        )
        lessons = []
        group_schedule_dao = GroupScheduleDAO(session=self._session)
        for schedule in schedules:
            present_students = await Visit.find(
                Visit.schedule_id == schedule.id,
                Visit.status == AttendanceStatus.PRESENT,
            ).count()
            number_of_students = await group_schedule_dao.get_number_of_students_in_groups(
                groups=[
                    gwn.id for gwn in schedule.groups_with_numbers
                ]
            )
            total_attendance = TotalAttendance(
                total_students=number_of_students,
                present_students=present_students,
            )
            schedule.student_data = None
            schedule.can_be_edited_by_prefect = await self.does_prefect_have_access_to_changing_statuses(
                schedule_id=schedule.id,
                group_id=None,
            )
            schedule.total_attendance = total_attendance

            lesson_data = lesson_pb2.Schedule(
                **BaseScheduleSchema.model_validate(
                    schedule
                ).model_dump(mode="json")
            )
            lessons.append(lesson_data)

        return lesson_service_pb2.LessonsResponse(lessons=lessons)

    async def get_lesson_details(
        self,
        user_id: uuid.UUID,
        schedule_id: uuid.UUID,
        context: grpc.aio.ServicerContext,
    ) -> lesson_service_pb2.LessonDetailsResponse:
        schedule, groups = await self.get_schedule_and_groups(
            schedule_id=schedule_id,
            user_id=user_id,
            context=context,
        )
        schedule.student_data = None
        schedule.can_be_edited_by_prefect = any(
            group.can_be_edited_by_prefect for group in groups
        )

        return lesson_service_pb2.LessonDetailsResponse(
            **FullScheduleDataSchema(
                schedule_data=BaseScheduleSchema.model_validate(
                    schedule
                ),
                groups=groups,
            ).model_dump(mode="json")
        )

    async def check_role_for_teacher_or_administrator(
        self,
        user_id: uuid.UUID,
        schedule_id: uuid.UUID,
        group_id: uuid.UUID | None,
        context: grpc.aio.ServicerContext,
    ):
        dao_obj = self.dao_class(self._session)
        has_access = (
            await dao_obj.does_teacher_have_group_in_schedule(
                teacher_id=user_id,
                schedule_id=schedule_id,
                group_id=group_id,
            )
        )
        if not has_access:
            await context.abort(
                grpc.StatusCode.PERMISSION_DENIED,
                "Вы не записаны на это занятие",
            )

    async def check_for_access_to_change_attendance(
        self,
        user_id: uuid.UUID,
        schedule_id: uuid.UUID,
        group_id: uuid.UUID,
        context: grpc.aio.ServicerContext,
    ) -> None:
        await self.check_role_for_teacher_or_administrator(
            user_id=user_id,
            schedule_id=schedule_id,
            group_id=group_id,
            context=context,
        )
