from typing import Annotated

import grpc.aio
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie
from starlette.status import HTTP_403_FORBIDDEN

from core import settings
from .stubs import UserStub
from core.grpc.pb import user_service_pb2
from core.schemas.user import UserData

cookie_scheme = APIKeyCookie(name=settings.auth.token_name)


async def get_current_user(
    user_stub: UserStub,
    token: Annotated[str, Depends(cookie_scheme)],
) -> UserData:
    try:
        user = await user_stub.UserAuth(
            user_service_pb2.AuthRequest(),
            metadata=(
                (
                    "authorization",
                    token,
                ),
            ),
        )
        return UserData.model_validate(user)
    except grpc.aio.AioRpcError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )


UserDep = Annotated[UserData, Depends(get_current_user)]
