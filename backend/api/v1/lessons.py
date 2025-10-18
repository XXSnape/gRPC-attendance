import asyncio
import datetime
import uuid
from typing import AsyncIterator

import grpc

from core.databases.sql.dao.student_group import StudentGroupDAO
from core.databases.sql.db_helper import db_helper
from core.dependencies.stubs import LessonStub
from core.dependencies.user import UserMetadataDep
from core.grpc.pb import lesson_service_pb2, lesson_pb2
from core.schemas import lesson
from fastapi import APIRouter, HTTPException, status
from loguru import logger

from services.lesson import create_attendances

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


@router.post(
    "/{lesson_id}/mark-attendance/",
    response_model=lesson.ReadLessonStudentAttendanceSchema,
)
async def mark_lesson_attendance(
    lesson_id: uuid.UUID,
    user_metadata: UserMetadataDep,
    stub: LessonStub,
    attendance_data: list[lesson.MarkStudentAttendanceSchema],
):
    # async with (
    #     db_helper.get_async_session_without_commit() as session
    # ):
    #     dao = StudentGroupDAO(session=session)
    #     student_group = await dao.get_group_by_student_id(
    #         user_id=uuid.UUID(user_metadata[0][1])
    #     )
    #     students_ids = [
    #         sg.student_id for sg in student_group.group.students
    #     ]
    #     print(students_ids)
    #     return lesson.ReadLessonStudentAttendanceSchema(
    #         attendances=[]
    #     )

    request_stream = create_attendances(
        attendance_data=attendance_data,
    )
    metadata = user_metadata + (("lesson_id", str(lesson_id)),)
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
        logger.exception(
            "Ошибка при обновлении посещаемости для пары с ID {}: {} {}",
            lesson_id,
            exc.code(),
            exc.details(),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновлении посещаемости",
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
        return lesson.FullLessonDataSchema.model_validate(response)
    except grpc.aio.AioRpcError as exc:
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
