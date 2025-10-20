import uuid
from collections.abc import AsyncIterator

import grpc
from beanie.odm.operators.update.general import Set

from core.databases.no_sql.documents.visit import Visit
from core.databases.sql.dao.schedule import GroupScheduleDAO
from core.databases.sql.dao.student_group import StudentGroupDAO
from core.databases.sql.db_helper import db_helper
from core.enums.status import AttendanceStatus
from core.grpc.pb import (
    lesson_pb2,
    lesson_service_pb2,
    lesson_service_pb2_grpc,
)
from core.grpc.utils.user import get_user_data_from_metadata
from core.schemas.attendance import AttendanceSchema
from core.schemas.lesson import (
    BaseScheduleSchema,
    FullScheduleDataSchema,
    StudentLessonSchema,
    GroupSchema,
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
            group_schedules = await dao.get_user_lessons(
                request.date, user.id
            )
            lessons = []
            for group_schedule in group_schedules:
                visit = await Visit.find_one(
                    Visit.schedule_id == group_schedule.schedule.id,
                    Visit.student_id == user.id,
                )

                student_data = StudentLessonSchema(
                    attendance=AttendanceSchema(
                        status=(
                            visit.status
                            if visit is not None
                            else AttendanceStatus.ABSENT
                        )
                    ),
                    group_id=group_schedule.group_id,
                )
                lesson_data = lesson_pb2.Schedule(
                    **BaseScheduleSchema(
                        id=group_schedule.schedule.id,
                        number=group_schedule.schedule.number,
                        type_of_lesson=group_schedule.schedule.type_of_lesson,
                        subgroup_number=group_schedule.subgroup_number,
                        lesson=group_schedule.schedule.lesson,
                        audience=group_schedule.schedule.audience,
                        teachers=group_schedule.schedule.teachers,
                        student_data=student_data,
                        can_be_edited_by_prefect=False,
                    ).model_dump(mode="json")
                )
                lessons.append(lesson_data)

            return lesson_service_pb2.LessonsResponse(
                lessons=lessons
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
        user_status = AttendanceSchema()
        subgroup_number = None
        user = await get_user_data_from_metadata(context)
        async with (
            db_helper.get_async_session_without_commit() as session
        ):
            dao = GroupScheduleDAO(session)
            result = await dao.get_lesson_details(
                user_id=user.id,
                schedule_id=request.schedule_id,
            )
            if result is None:
                await context.abort(
                    grpc.StatusCode.NOT_FOUND,
                    "Пара не найдена в расписании вашей группы",
                )
            schedule, user_group_id = result

            groups = []
            documents = await Visit.find(
                Visit.schedule_id == uuid.UUID(request.schedule_id)
            ).to_list()
            user_uuid = uuid.UUID(user.id)
            for (
                group_with_subgroup
            ) in schedule.groups_with_subgroups:
                if group_with_subgroup.group_id == user_group_id:
                    subgroup_number = (
                        group_with_subgroup.subgroup_number
                    )
                group_with_number = (
                    group_with_subgroup.group_with_number
                )
                group_schema = GroupSchema(
                    id=group_with_number.id,
                    complete_name=group_with_number.complete_name,
                    attendances=[],
                )
                groups.append(group_schema)
                if group_with_number.id == user_group_id:

                    group_attendances = []
                    for (
                        student_with_group
                    ) in group_with_number.students_with_groups:
                        if (
                            student_with_group.student_id
                            == user_uuid
                        ):
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
                                    == user_uuid
                                ):
                                    user_status.status = (
                                        document.status
                                    )
                                break
                        group_attendances.append(schema)
                    group_schema.attendances = group_attendances

            student_data = StudentLessonSchema(
                attendance=user_status,
                group_id=user_group_id,
                is_prefect=is_current_user_prefect,
            )
            schedule_data = BaseScheduleSchema(
                id=schedule.id,
                number=schedule.number,
                type_of_lesson=schedule.type_of_lesson,
                subgroup_number=subgroup_number,
                lesson=schedule.lesson,
                audience=schedule.audience,
                teachers=schedule.teachers,
                student_data=student_data,
                can_be_edited_by_prefect=False,
            )

            return lesson_service_pb2.LessonDetailsResponse(
                **FullScheduleDataSchema(
                    schedule_data=schedule_data,
                    groups=groups,
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
