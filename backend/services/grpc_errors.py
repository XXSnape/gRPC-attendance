from typing import NoReturn

from grpc import StatusCode
from fastapi import status, HTTPException
from grpc.aio import AioRpcError
from loguru import logger


def catch_errors(
    error: AioRpcError,
    failure_message: str = "Произошла ошибка, попробуйте позже.",
) -> NoReturn:
    mapping = {
        StatusCode.CANCELLED: status.HTTP_408_REQUEST_TIMEOUT,
        StatusCode.INVALID_ARGUMENT: status.HTTP_422_UNPROCESSABLE_ENTITY,
        StatusCode.DEADLINE_EXCEEDED: status.HTTP_408_REQUEST_TIMEOUT,
        StatusCode.NOT_FOUND: status.HTTP_404_NOT_FOUND,
        StatusCode.ALREADY_EXISTS: status.HTTP_409_CONFLICT,
        StatusCode.PERMISSION_DENIED: status.HTTP_403_FORBIDDEN,
        StatusCode.UNAUTHENTICATED: status.HTTP_401_UNAUTHORIZED,
        StatusCode.RESOURCE_EXHAUSTED: status.HTTP_429_TOO_MANY_REQUESTS,
        StatusCode.ABORTED: status.HTTP_409_CONFLICT,
    }
    http_code = mapping.get(error.code())
    if http_code:
        raise HTTPException(
            status_code=http_code,
            detail=error.details(),
        )
    logger.exception(
        "Произошла неизвестная ошибка: {} {}\n\nС сообщением: {}",
        error.code(),
        error.details(),
        failure_message,
    )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=failure_message,
    )
