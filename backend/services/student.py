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
    GroupSchema,
    FullScheduleDataSchema,
)
from core.schemas.user import UserAttendanceSchema

from .base import BaseService


class StudentService(BaseService):
    dao_class = GroupScheduleDAO

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
        is_current_user_prefect = False
        user_status = AttendanceSchema()
        dao_obj = self.dao_class(self._session)
        schedule = await dao_obj.get_lesson_details(
            user_id=user_id,
            schedule_id=schedule_id,
        )
        if schedule is None:
            await context.abort(
                grpc.StatusCode.NOT_FOUND,
                "Пара не найдена в расписании вашей группы",
            )
        student_group_id = await dao_obj.get_group_id_by_student(
            user_id
        )

        groups = []
        documents = await Visit.find(
            Visit.schedule_id == schedule_id
        ).to_list()
        for group_with_number in schedule.groups_with_numbers:
            group_schema = GroupSchema(
                id=group_with_number.id,
                complete_name=group_with_number.complete_name,
                attendances=[],
            )
            groups.append(group_schema)
            if group_with_number.id == student_group_id:
                group_attendances = []
                for (
                    student_with_group
                ) in group_with_number.students_with_groups:
                    if student_with_group.student_id == user_id:
                        is_current_user_prefect = (
                            student_with_group.is_prefect
                        )

                    schema = UserAttendanceSchema(
                        full_name=student_with_group.student.full_name,
                        decryption_of_full_name=student_with_group.student.decryption_of_full_name,
                        personal_number=student_with_group.student.personal_number,
                        is_prefect=student_with_group.is_prefect,
                        student_id=student_with_group.student_id,
                    )
                    for document in documents:
                        if (
                            document.student_id
                            == student_with_group.student_id
                        ):
                            schema.attendance.status = (
                                document.status
                            )
                            if (
                                student_with_group.student_id
                                == user_id
                            ):
                                user_status.status = document.status
                            break
                    group_attendances.append(schema)
                group_schema.attendances = group_attendances

        student_data = StudentLessonSchema(
            attendance=user_status,
            group_id=student_group_id,
            is_prefect=is_current_user_prefect,
        )
        schedule.student_data = student_data
        schedule.can_be_edited_by_prefect = False
        schedule.total_attendance = None
        schedule.group_names = [
            group.complete_name for group in groups
        ]
        schedule_data = BaseScheduleSchema.model_validate(schedule)
        return lesson_service_pb2.LessonDetailsResponse(
            **FullScheduleDataSchema(
                schedule_data=schedule_data,
                groups=groups,
            ).model_dump(mode="json")
        )
