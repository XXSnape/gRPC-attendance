import grpc
from core.schemas.user import UserDataSchema
from pydantic import ValidationError


async def get_user_data_from_metadata(
    context: grpc.aio.ServicerContext,
) -> UserDataSchema:
    metadata = dict(context.invocation_metadata())
    try:
        return UserDataSchema.model_validate(metadata)
    except ValidationError:
        await context.abort(
            grpc.StatusCode.UNAUTHENTICATED,
            details="Необходимо авторизоваться",
        )
