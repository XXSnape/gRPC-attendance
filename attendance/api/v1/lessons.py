import datetime

import grpc
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from google.protobuf.json_format import MessageToDict
from loguru import logger
from pydantic import TypeAdapter

from core import settings
from core.databases.sql.dao.schedule import GroupScheduleDAO
from core.databases.sql.db_helper import db_helper
from core.dependencies.stubs import UserStub, LessonStub
from core.dependencies.user import UserDep
from core.grpc.pb import user_service_pb2, lesson_service_pb2
from core.schemas import lesson

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
