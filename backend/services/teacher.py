import datetime
import uuid

from core.databases.no_sql.documents import Visit
from core.databases.sql.dao.group_schedule import GroupScheduleDAO
from core.databases.sql.dao.teacher_schedule import (
    TeacherScheduleDAO,
)
from core.enums.status import AttendanceStatus
from core.grpc.pb import lesson_service_pb2, lesson_pb2
from core.schemas.lesson import TotalAttendance, BaseScheduleSchema

from .base import BaseService


class TeacherService(BaseService):
    dao_class = TeacherScheduleDAO

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

            lesson_data = lesson_pb2.Schedule(
                **BaseScheduleSchema(
                    id=schedule.id,
                    number=schedule.number,
                    date=schedule.date,
                    type_of_lesson=schedule.type_of_lesson,
                    subgroup_number=schedule.subgroup_number,
                    is_standardized=schedule.is_standardized,
                    lesson=schedule.lesson,
                    audiences=schedule.audiences,
                    teachers=schedule.teachers,
                    student_data=None,
                    can_be_edited_by_prefect=False,
                    group_names=[
                        gwn.complete_name
                        for gwn in schedule.groups_with_numbers
                    ],
                    total_attendance=total_attendance,
                ).model_dump(mode="json")
            )
            lessons.append(lesson_data)

        return lesson_service_pb2.LessonsResponse(lessons=lessons)
