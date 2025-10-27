import datetime
import uuid
from typing import AsyncIterator

import grpc
from core.dependencies.stubs import LessonStub
from core.dependencies.user import UserMetadataDep
from core.grpc.pb import lesson_pb2, lesson_service_pb2
from core.schemas import lesson
from fastapi import APIRouter
from loguru import logger
from utils.grpc_errors import catch_errors
from utils.lesson import create_attendances

router = APIRouter(tags=["Пары"])


@router.get(
    "/",
    response_model=lesson.LessonsDataSchema,
)
async def get_lessons_by_date(
    date: datetime.date,
    user_metadata: UserMetadataDep,
    stub: LessonStub,
):
    request = lesson_service_pb2.LessonsRequest(
        date=str(date),
    )
    try:
        response = await stub.GetLessons(
            request,
            metadata=user_metadata,
        )
        return lesson.LessonsDataSchema(lessons=response.lessons)
    except grpc.aio.AioRpcError as exc:
        logger.error(
            "Ошибка при получении пар на дату {}: {} {}",
            date,
            exc.code(),
            exc.details(),
        )
        catch_errors(
            exc,
            "Ошибка при получении пар",
        )


@router.get(
    "/study-days/",
    response_model=lesson.StudyDaysSchema,
)
async def get_study_days(
    year: int,
    month: int,
    user_metadata: UserMetadataDep,
    stub: LessonStub,
):
    request = lesson_service_pb2.LessonsForMonthRequest(
        year=year,
        month=month,
    )
    try:
        response = await stub.GetLessonsForMonth(
            request,
            metadata=user_metadata,
        )
        return lesson.StudyDaysSchema(dates=response.dates)
    except grpc.aio.AioRpcError as exc:
        logger.error(
            "Ошибка при получении учебных дней на {}/{}: {} {}",
            month,
            year,
            exc.code(),
            exc.details(),
        )
        catch_errors(
            exc,
            "Ошибка при получении учебных дней",
        )


@router.put(
    "/{schedule_id}/groups/{group_id}/attendance/",
    response_model=lesson.ReadLessonStudentAttendanceSchema,
)
async def mark_lesson_attendance(
    schedule_id: uuid.UUID,
    group_id: uuid.UUID,
    user_metadata: UserMetadataDep,
    stub: LessonStub,
    attendance_data: list[lesson.MarkStudentAttendanceSchema],
):

    request_stream = create_attendances(
        attendance_data=attendance_data,
    )
    metadata = user_metadata + (
        ("schedule_id", str(schedule_id)),
        ("group_id", str(group_id)),
    )
    try:
        response_stream: AsyncIterator[
            lesson_pb2.StudentAttendance
        ] = stub.SetStudentAttendance(
            request_stream,
            metadata=metadata,
        )
        attendances = []
        async for response in response_stream:
            attendances.append(response)
        return lesson.ReadLessonStudentAttendanceSchema(
            attendances=attendances
        )
    except grpc.aio.AioRpcError as exc:
        logger.error(
            "Ошибка при обновлении посещаемости для пары с ID {}: {} {}",
            schedule_id,
            exc.code(),
            exc.details(),
        )
        catch_errors(
            exc,
            "Ошибка при обновлении посещаемости",
        )


@router.get(
    "/{schedule_id}/",
    response_model=lesson.FullScheduleDataSchema,
)
async def get_schedule_by_id(
    schedule_id: uuid.UUID,
    user_metadata: UserMetadataDep,
    stub: LessonStub,
):

    request = lesson_service_pb2.LessonDetailsRequest(
        schedule_id=str(schedule_id),
    )
    try:
        response = await stub.GetLessonDetails(
            request,
            metadata=user_metadata,
        )
        return lesson.FullScheduleDataSchema.model_validate(response)
    except grpc.aio.AioRpcError as exc:
        logger.error(
            "Ошибка при получении детали пары с ID {}: {} {}",
            schedule_id,
            exc.code(),
            exc.details(),
        )
        catch_errors(
            exc,
            "Ошибка при получении деталей пары",
        )
