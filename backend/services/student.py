import datetime
import uuid

import grpc
from beanie.odm.operators.find.comparison import In

from core import settings
from core.databases.no_sql.documents import (
    Visit,
    QRCode,
    TrackingAttendance,
)
from core.databases.sql.dao.group_schedule import GroupScheduleDAO
from core.enums.status import AttendanceStatus
from core.grpc.pb import lesson_pb2, lesson_service_pb2
from core.schemas.attendance import AttendanceSchema
from core.schemas.lesson import (
    StudentLessonSchema,
    BaseScheduleSchema,
    TotalAttendance,
    FullScheduleDataSchema,
)
from utils.dt import generate_utc_dt

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
            schedule.can_be_edited_by_prefect = await self.does_prefect_have_access_to_changing_statuses(
                group_id=group_id,
                schedule_id=schedule.id,
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
        student_group_id = await self.dao_class(
            session=self._session
        ).get_group_id_by_student(user_id)
        student_data = StudentLessonSchema(
            attendance=AttendanceSchema(),
            group_id=student_group_id,
            is_prefect=False,
        )
        for group in groups:
            for user_attendance in group.attendances:
                if user_attendance.student_id == user_id:
                    student_data.attendance.status = (
                        user_attendance.attendance.status
                    )
                    student_data.is_prefect = (
                        user_attendance.is_prefect
                    )
                    break
        schedule.student_data = student_data
        schedule.can_be_edited_by_prefect = any(
            group.can_be_edited_by_prefect
            for group in groups
            if group.id == student_group_id
        )
        return lesson_service_pb2.LessonDetailsResponse(
            **FullScheduleDataSchema(
                schedule_data=BaseScheduleSchema.model_validate(
                    schedule
                ),
                groups=groups,
            ).model_dump(mode="json")
        )

    async def check_for_access_to_change_attendance(
        self,
        user_id: uuid.UUID,
        schedule_id: uuid.UUID,
        group_id: uuid.UUID,
        context: grpc.aio.ServicerContext,
    ) -> None:
        dao_obj = self.dao_class(session=self._session)
        is_prefect = await dao_obj.check_is_prefect_in_group(
            group_id=group_id,
            student_id=user_id,
        )
        if not is_prefect:
            await context.abort(
                grpc.StatusCode.PERMISSION_DENIED,
                "Пользователь не является старостой группы",
            )
        has_access = (
            await self.does_prefect_have_access_to_changing_statuses(
                group_id=group_id,
                schedule_id=schedule_id,
            )
        )
        if not has_access:
            await context.abort(
                grpc.StatusCode.PERMISSION_DENIED,
                "У старосты группы нет активного доступа для изменения посещаемости этой пары",
            )

    async def check_role_for_teacher_or_administrator(
        self,
        user_id: uuid.UUID,
        schedule_id: uuid.UUID,
        group_id: uuid.UUID | None,
        context: grpc.aio.ServicerContext,
    ):
        await context.abort(
            grpc.StatusCode.PERMISSION_DENIED,
            "Функция недоступна для студентов.",
        )

    async def approve_attendance_by_token(
        self,
        student_id: uuid.UUID,
        token: str,
        context: grpc.aio.ServicerContext,
    ) -> None:
        dao_obj = self.dao_class(session=self._session)
        now = generate_utc_dt()
        qr_code_could_have_been_created_at = (
            now
            - datetime.timedelta(
                seconds=settings.app.validity_period_of_qr_code,
            )
        )
        qr_code_document = await QRCode.find_one(
            QRCode.token == token,
            QRCode.created_at >= qr_code_could_have_been_created_at,
        )
        if qr_code_document is None:
            await context.abort(
                grpc.StatusCode.PERMISSION_DENIED,
                "Невозможно подтвердить посещаемость: неверные данные QR-кода "
                "или время для подтверждения истекло.",
            )
        if not dao_obj.check_student_schedule(
            student_id=student_id,
            schedule_id=qr_code_document.schedule_id,
        ):
            await context.abort(
                grpc.StatusCode.PERMISSION_DENIED,
                "Студент не записан на данную пару.",
            )
        visit_document = await Visit.find_one(
            Visit.student_id == student_id,
            Visit.schedule_id == qr_code_document.schedule_id,
        )
        if visit_document:
            if visit_document.status == AttendanceStatus.PRESENT:
                return
            if (
                visit_document.status
                == AttendanceStatus.SKIP_RESPECTFULLY
            ):
                await context.abort(
                    grpc.StatusCode.PERMISSION_DENIED,
                    "Посещаемость уже была подтверждена с оправданной причиной.",
                )
            visit_document.status = AttendanceStatus.PRESENT
            await visit_document.save()
        else:
            await Visit(
                student_id=student_id,
                schedule_id=qr_code_document.schedule_id,
                status=AttendanceStatus.PRESENT,
            ).insert()
        await TrackingAttendance(
            student_id=student_id,
            schedule_id=qr_code_document.schedule_id,
            user_id_changed_status=student_id,
            status=AttendanceStatus.PRESENT,
        ).insert()
