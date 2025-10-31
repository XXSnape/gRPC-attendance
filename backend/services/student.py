import datetime
import uuid

import grpc
from beanie.odm.operators.find.comparison import In

from core.databases.no_sql.documents import Visit
from core.databases.sql.dao.group_schedule import GroupScheduleDAO
from core.enums.status import AttendanceStatus
from core.grpc.pb import lesson_pb2, lesson_service_pb2
from core.schemas.attendance import AttendanceSchema
from core.schemas.lesson import (
    StudentLessonSchema,
    BaseScheduleSchema,
    TotalAttendance,
)

from .base import BaseService


class StudentService(BaseService):
    dao_class = GroupScheduleDAO
    can_t_view_lesson_details = (
        "Пара не найдена в расписании вашей группы."
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
        if not schedules:
            return lesson_service_pb2.LessonsResponse(lessons=[])
        group_id = await dao_obj.get_group_id_by_student(
            student_id=user_id
        )
        is_student_prefect = await dao_obj.is_student_prefect(
            student_id=user_id,
            group_id=group_id,
        )
        students_in_group = []
        if is_student_prefect:
            students_in_group = await dao_obj.get_students_in_group(
                group_id=group_id
            )

        lessons = []
        for schedule in schedules:
            total_attendance = None
            visit = await Visit.find_one(
                Visit.schedule_id == schedule.id,
                Visit.student_id == user_id,
            )
            student_data = StudentLessonSchema(
                attendance=AttendanceSchema(
                    status=(
                        visit.status
                        if visit is not None
                        else AttendanceStatus.ABSENT
                    )
                ),
                group_id=group_id,
            )
            if students_in_group:
                present_students = await Visit.find(
                    Visit.schedule_id == schedule.id,
                    In(Visit.student_id, students_in_group),
                    Visit.status == AttendanceStatus.PRESENT,
                ).count()
                total_attendance = TotalAttendance(
                    total_students=len(students_in_group),
                    present_students=present_students,
                )
            schedule.student_data = student_data
            schedule.can_be_edited_by_prefect = False
            schedule.group_names = [
                gwn.complete_name
                for gwn in schedule.groups_with_numbers
            ]
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
        student_group_id = await self.dao_class(
            session=self._session
        ).get_group_id_by_student(user_id)
        if not student_group_id:
            await context.abort(
                grpc.StatusCode.NOT_FOUND,
                "Вы не состоите ни в одной группе",
            )
        return await self.get_groups_and_attendances(
            schedule_id=schedule_id,
            user_id=user_id,
            context=context,
            student_group_id=student_group_id,
        )
