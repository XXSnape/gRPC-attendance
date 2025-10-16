import grpc
from core import settings
from core.dependencies.stubs import UserStub
from core.dependencies.user import UserDep
from core.grpc.pb import user_service_pb2
from core.schemas import user
from fastapi import APIRouter, HTTPException, status
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
    print("content", content)
    http_response = JSONResponse(content)
    http_response.set_cookie(
        key=settings.auth.token_name,
        value=grpc_response.token,
        httponly=True,
        expires=settings.auth.token_duration,
        samesite="strict",
    )
    return http_response


@router.get("/me/", response_model=user.UserDataSchema)
async def get_me(current_user: UserDep):
    return current_user
