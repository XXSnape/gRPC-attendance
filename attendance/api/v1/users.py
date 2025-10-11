from fastapi import APIRouter

from core.dependencies.stubs import UserStub
from core.grpc.pb import user_service_pb2
from core.schemas import user

router = APIRouter(tags=["Пользователи"])


@router.post("/sign-in/", response_model=user.UserSignedUpSchema)
async def sign_in(
    user_in: user.UserInSchema,
    stub: UserStub,
):
    request = user_service_pb2.SingInRequest(**user_in.model_dump())
    response = await stub.UserSingIn(request)
    print(response, type(response))
    return response
    return MessageT

    print("type(stab)", type(stab))
    return {"message": "User created"}
