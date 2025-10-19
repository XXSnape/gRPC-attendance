from typing import Annotated

import grpc
from core import settings
from core.dependencies.stubs import UserStub
from core.dependencies.user import UserDep, cookie_scheme
from core.grpc.pb import user_service_pb2
from core.schemas import user
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Response,
    Depends,
)
from fastapi.responses import JSONResponse
from google.protobuf.json_format import MessageToDict
from loguru import logger

router = APIRouter(tags=["Пользователи"])


@router.post(
    "/sign-in/",
    response_model=user.UserDataSchema,
)
async def sign_in(
    user_in: user.UserInSchema,
    stub: UserStub,
):
    grpc_request = user_service_pb2.SingInRequest(
        **user_in.model_dump()
    )
    try:
        grpc_response = await stub.UserSingIn(grpc_request)
    except grpc.aio.AioRpcError as exc:
        logger.debug(
            "Попытка входа с неверным логином или паролем: {} {} {}",
            user_in,
            exc.code(),
            exc.details(),
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )
    content = MessageToDict(
        grpc_response.user,
        preserving_proto_field_name=True,
    )
    http_response = JSONResponse(content)
    http_response.set_cookie(
        key=settings.auth.token_name,
        value=grpc_response.token,
        httponly=True,
        expires=settings.auth.token_duration,
        samesite="strict",
    )
    return http_response


@router.post(
    "/sign-out/",
)
async def sign_out(
    token: Annotated[str, Depends(cookie_scheme)],
    stub: UserStub,
):
    grpc_request = user_service_pb2.LogoutRequest(
        token=token,
    )
    try:
        await stub.UserLogout(grpc_request)
    except grpc.aio.AioRpcError as exc:
        logger.error(
            "Ошибка при выходе пользователя: {} {}",
            exc.code(),
            exc.details(),
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.details(),
        )
    response = Response()
    response.delete_cookie(
        key=settings.auth.token_name,
    )
    return response


@router.get("/me/", response_model=user.UserDataSchema)
async def get_me(current_user: UserDep):
    return current_user
