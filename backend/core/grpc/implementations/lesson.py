import uuid
from collections.abc import AsyncIterator

import grpc
from beanie.odm.operators.update.general import Set
from beanie.operators import In

from core.databases.no_sql.documents.visit import Visit
from core.databases.sql.dao.schedule import GroupScheduleDAO
from core.databases.sql.dao.student_group import StudentGroupDAO
from core.databases.sql.db_helper import db_helper
from core.grpc.pb import (
    lesson_pb2,
    lesson_service_pb2,
    lesson_service_pb2_grpc,
)
from core.grpc.utils.user import get_user_data_from_metadata
from core.schemas.attendance import AttendanceSchema
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
        is_current_user_prefect = False
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
            documents = await Visit.find(
                Visit.lesson_id == uuid.UUID(request.lesson_id)
            ).to_list()
            attendances = []
            user_uuid = uuid.UUID(user.id)
            for (
                student_with_group
            ) in lesson.group.students_with_groups:
                if student_with_group.student_id == user_uuid:
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
                        schema.attendance.status = document.status
                        break
                attendances.append(schema)
            return lesson_service_pb2.LessonDetailsResponse(
                **FullLessonDataSchema(
                    schedule_data=BaseScheduleSchema.model_validate(
                        lesson
                    ),
                    group=lesson.group,
                    attendances=attendances,
                    is_prefect=is_current_user_prefect,
                ).model_dump(mode="json")
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
        lesson_id = metadata.get("lesson_id")
        async with (
            db_helper.get_async_session_without_commit() as session
        ):
            dao = StudentGroupDAO(session=session)
            student_group = await dao.get_group_by_student_id(
                user_id=user.id
            )
            if student_group is None:
                await context.abort(
                    grpc.StatusCode.NOT_FOUND,
                    "Группа студента не найдена или он не является старостой",
                )
                return
            check = await GroupScheduleDAO(
                session=session
            ).check_group_has_lesson(
                lesson_id=lesson_id,
                group_id=student_group.group_id,
            )

            if not lesson_id or not check:
                await context.abort(
                    grpc.StatusCode.NOT_FOUND,
                    "Пара не найдена в расписании вашей группы",
                )
                return
            students_ids = [
                sg.student_id
                for sg in student_group.group_with_number.students_with_groups
            ]

        async for request in request_iterator:
            if uuid.UUID(request.student_id) in students_ids:
                await Visit.find_one(
                    Visit.lesson_id == uuid.UUID(lesson_id),
                    Visit.student_id
                    == uuid.UUID(request.student_id),
                ).upsert(
                    Set({Visit.status: request.attendance.status}),
                    on_insert=Visit(
                        lesson_id=uuid.UUID(lesson_id),
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
