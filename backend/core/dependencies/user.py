from typing import Annotated

import grpc.aio
from core import settings
from core.grpc.pb import user_service_pb2
from core.schemas.user import UserDataSchema
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie
from starlette.status import HTTP_403_FORBIDDEN

from .stubs import UserStub

cookie_scheme = APIKeyCookie(name=settings.auth.token_name)


async def get_current_user(
    user_stub: UserStub,
    token: Annotated[str, Depends(cookie_scheme)],
) -> UserDataSchema:
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
        return UserDataSchema.model_validate(user)
    except grpc.aio.AioRpcError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )


def get_user_metadata(
    user_data: Annotated[UserDataSchema, Depends(get_current_user)],
) -> tuple[tuple[str, str], ...]:
    metadata = tuple(
        (str(k), str(v))
        for k, v in user_data.model_dump(
            exclude={"full_name"}
        ).items()
    )
    return metadata


UserDep = Annotated[UserDataSchema, Depends(get_current_user)]
UserMetadataDep = Annotated[
    tuple[tuple[str, str], ...],
    Depends(get_user_metadata),
]
