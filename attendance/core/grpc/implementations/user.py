import grpc

from core.grpc.pb import user_pb2
from core.grpc.pb import user_service_pb2
from core.grpc.pb import user_service_pb2_grpc


class UserServiceServicer(
    user_service_pb2_grpc.UserServiceServicer,
):
    async def UserSingIn(
        self,
        request: user_service_pb2.SingInRequest,
        context: grpc.aio.ServicerContext,
    ) -> user_service_pb2.SingInResponse:
        return user_service_pb2.SingInResponse(
            token="abc",
            user=user_pb2.UserData(
                type="student",
                full_name="John Doe",
            ),
        )
