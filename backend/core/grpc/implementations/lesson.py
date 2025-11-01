import datetime
import uuid
from collections.abc import AsyncIterator

import grpc
from beanie.odm.operators.update.general import Set
from core.databases.no_sql.documents.visit import Visit
from core.databases.sql.dao.group_schedule import GroupScheduleDAO
from core.databases.sql.db_helper import db_helper
from core.grpc.pb import (
    lesson_pb2,
    lesson_service_pb2,
    lesson_service_pb2_grpc,
)
from core.grpc.utils.user import get_user_data_from_metadata
from core.schemas.attendance import AttendanceSchema


class LessonServiceServicer(
    lesson_service_pb2_grpc.LessonServiceServicer,
):
    async def GetLessons(
        self,
        request: lesson_service_pb2.LessonsRequest,
        context: grpc.aio.ServicerContext,
    ) -> lesson_service_pb2.LessonsResponse:
        user = await get_user_data_from_metadata(context)
        service = user.get_service_by_role()
        async with (
            db_helper.get_async_session_without_commit() as session
        ):
            date = datetime.date.fromisoformat(request.date)
            service_obj = service(session)
            return await service_obj.get_schedule_by_date(
                date=date,
                user_id=user.id,
            )

    async def GetLessonsForMonth(
        self,
        request: lesson_service_pb2.LessonsForMonthRequest,
        context: grpc.aio.ServicerContext,
    ) -> lesson_service_pb2.LessonsForMonthResponse:
        user = await get_user_data_from_metadata(context)
        service = user.get_service_by_role()
        async with (
            db_helper.get_async_session_without_commit() as session
        ):
            service_obj = service(session)
            response = await service_obj.get_user_lessons_for_month(
                month=request.month,
                year=request.year,
                user_id=user.id,
            )
            return response

    async def GetLessonDetails(
        self,
        request: lesson_service_pb2.LessonDetailsRequest,
        context: grpc.aio.ServicerContext,
    ) -> lesson_service_pb2.LessonDetailsResponse:
        user = await get_user_data_from_metadata(context)
        service = user.get_service_by_role()
        async with (
            db_helper.get_async_session_without_commit() as session
        ):
            service_obj = service(session)
            return await service_obj.get_lesson_details(
                user_id=user.id,
                schedule_id=uuid.UUID(request.schedule_id),
                context=context,
            )

    async def SetStudentAttendance(
        self,
        request_iterator: AsyncIterator[
            lesson_service_pb2.StudentAttendanceRequest
        ],
        context: grpc.aio.ServicerContext,
    ) -> AsyncIterator[lesson_service_pb2.StudentAttendanceResponse]:
        user = await get_user_data_from_metadata(context)
        metadata = dict(context.invocation_metadata())
        schedule_id = metadata.get("schedule_id")
        group_id = metadata.get("group_id")
        if schedule_id is None or group_id is None:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Отсутствуют необходимые метаданные: schedule_id или group_id",
            )
            return
        async with (
            db_helper.get_async_session_without_commit() as session
        ):
            dao = GroupScheduleDAO(session=session)
            is_prefect = await dao.check_is_prefect_in_group(
                group_id=group_id, user_id=user.id
            )
            if not is_prefect:
                await context.abort(
                    grpc.StatusCode.PERMISSION_DENIED,
                    "Пользователь не является старостой группы или не имеет прав на изменение посещаемости",
                )
            group_schedule = await dao.get_students_of_group(
                schedule_id=schedule_id,
                group_id=group_id,
            )
            students_with_groups = (
                group_schedule.group_with_number.students_with_groups
            )
            students_ids = [
                sg.student_id for sg in students_with_groups
            ]

        async for request in request_iterator:
            if uuid.UUID(request.student_id) in students_ids:
                await Visit.find_one(
                    Visit.schedule_id == uuid.UUID(schedule_id),
                    Visit.student_id
                    == uuid.UUID(request.student_id),
                ).upsert(
                    Set({Visit.status: request.attendance.status}),
                    on_insert=Visit(
                        schedule_id=uuid.UUID(schedule_id),
                        student_id=uuid.UUID(request.student_id),
                        status=request.attendance.status,
                    ),
                )

                yield lesson_service_pb2.StudentAttendanceResponse(
                    student_id=request.student_id,
                    attendance=lesson_pb2.Attendance(
                        **AttendanceSchema(
                            status=request.attendance.status
                        ).model_dump(mode="json")
                    ),
                )
