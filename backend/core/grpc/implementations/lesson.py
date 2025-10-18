import asyncio
import datetime
import uuid
from collections.abc import AsyncIterator

import grpc


from core.databases.sql.dao.schedule import GroupScheduleDAO
from core.databases.sql.db_helper import db_helper
from core.grpc.pb import (
    lesson_pb2,
    lesson_service_pb2,
    lesson_service_pb2_grpc,
)
from core.grpc.utils.user import get_user_data_from_metadata
from core.schemas.lesson import (
    BaseScheduleSchema,
    FullLessonDataSchema,
)
from core.schemas.user import UserAttendanceSchema


class LessonServiceServicer(
    lesson_service_pb2_grpc.LessonServiceServicer,
):
    async def GetLessons(
        self,
        request: lesson_service_pb2.LessonsRequest,
        context: grpc.aio.ServicerContext,
    ) -> lesson_service_pb2.LessonsResponse:
        user = await get_user_data_from_metadata(context)
        async with (
            db_helper.get_async_session_without_commit() as session
        ):
            dao = GroupScheduleDAO(session)
            lessons = await dao.get_user_lessons(
                request.date, user.id
            )
            return lesson_service_pb2.LessonsResponse(
                lessons=[
                    lesson_pb2.Schedule(
                        **BaseScheduleSchema.model_validate(
                            lesson
                        ).model_dump(mode="json")
                    )
                    for lesson in lessons
                ]
            )

    async def GetLessonsForMonth(
        self,
        request: lesson_service_pb2.LessonsForMonthRequest,
        context: grpc.aio.ServicerContext,
    ) -> lesson_service_pb2.LessonsForMonthResponse:
        user = await get_user_data_from_metadata(context)
        async with (
            db_helper.get_async_session_without_commit() as session
        ):
            dao = GroupScheduleDAO(session)
            dates = await dao.get_user_lessons_for_month(
                month=request.month,
                year=request.year,
                user_id=user.id,
            )
            return lesson_service_pb2.LessonsForMonthResponse(
                dates=[str(date) for date in dates]
            )

    async def GetLessonDetails(
        self,
        request: lesson_service_pb2.LessonDetailsRequest,
        context: grpc.aio.ServicerContext,
    ) -> lesson_service_pb2.LessonDetailsResponse:
        user = await get_user_data_from_metadata(context)
        async with (
            db_helper.get_async_session_without_commit() as session
        ):
            dao = GroupScheduleDAO(session)
            lesson = await dao.get_user_lessons(
                date=None,
                user_id=user.id,
                lesson_id=request.lesson_id,
            )
            return lesson_service_pb2.LessonDetailsResponse(
                **FullLessonDataSchema(
                    schedule_data=BaseScheduleSchema.model_validate(
                        lesson
                    ),
                    group=lesson.group,
                    attendances=[
                        UserAttendanceSchema(
                            full_name="dad",
                            decryption_of_full_name="wadwad",
                            personal_number="123",
                            is_prefect=False,
                            user_id=uuid.UUID(
                                "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                            ),
                        )
                    ],
                ).model_dump(mode="json")
            )

    async def SetStudentAttendance(
        self,
        request_iterator: AsyncIterator[
            lesson_service_pb2.StudentAttendanceRequest
        ],
        context: grpc.aio.ServicerContext,
    ) -> AsyncIterator[lesson_pb2.StudentAttendance]:
        async for request in request_iterator:
            yield lesson_pb2.StudentAttendance(
                full_name="dad",
                decryption_of_full_name="wadwad",
                personal_number="123",
                is_prefect=False,
                user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            )
