import datetime
import uuid

import grpc
from core.dependencies.stubs import LessonStub
from core.dependencies.user import UserDep, UserMetadataDep
from core.grpc.pb import lesson_service_pb2
from core.schemas import lesson
from fastapi import APIRouter, HTTPException, status
from loguru import logger

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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении пар",
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении учебных дней",
        )


@router.get(
    "/{lesson_id}/",
    response_model=lesson.FullLessonDataSchema,
)
async def get_lesson_by_id(
    lesson_id: uuid.UUID,
    user_metadata: UserMetadataDep,
    stub: LessonStub,
):
    request = lesson_service_pb2.LessonDetailsRequest(
        lesson_id=str(lesson_id),
    )
    try:
        response = await stub.GetLessonDetails(
            request,
            metadata=user_metadata,
        )
        return lesson.FullLessonDataSchema(
            schedule_data=response.schedule_data,
            group=response.group,
            attendances=response.attendances,
        )
    except grpc.aio.AioRpcError as exc:
        logger.exception("errr")
        logger.error(
            "Ошибка при получении детали пары с ID {}: {} {}",
            lesson_id,
            exc.code(),
            exc.details(),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении детали пары",
        )
