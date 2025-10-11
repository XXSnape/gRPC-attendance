import grpc
from fastapi import APIRouter, HTTPException
from loguru import logger
from starlette import status

from core.dependencies.stubs import UserStub
from core.grpc.pb import user_service_pb2
from core.schemas import user

router = APIRouter(tags=["Пользователи"])


@router.post(
    "/sign-in/",
    response_model=user.UserSignedUpSchema,
)
async def sign_in(
    user_in: user.UserInSchema,
    stub: UserStub,
):
    request = user_service_pb2.SingInRequest(**user_in.model_dump())
    try:
        response = await stub.UserSingIn(request)
        return response
    except grpc.aio.AioRpcError as exc:
        logger.debug(
            "Попытка входа с неверным логином или паролем: {} {}",
            exc.code(),
            exc.details(),
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )
