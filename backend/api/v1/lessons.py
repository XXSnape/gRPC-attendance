import datetime

import grpc
from core.dependencies.stubs import LessonStub
from core.dependencies.user import UserDep
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
    user: UserDep,
    stub: LessonStub,
):
    request = lesson_service_pb2.LessonsRequest(
        date=str(date),
    )
    try:
        metadata = tuple(
            (str(k), str(v))
            for k, v in user.model_dump(
                exclude={"full_name"}
            ).items()
        )
        print(metadata, type(metadata))
        response = await stub.GetLessons(
            request,
            metadata=metadata,
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
