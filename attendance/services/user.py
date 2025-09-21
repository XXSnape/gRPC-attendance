from core.pb import user_service_pb2_grpc, user_service_pb2
import grpc


class UserServiceServicer(
    user_service_pb2_grpc.UserServiceServicer,
):
    async def CreateUser(
        self,
        request: user_service_pb2.NewUserRequest,
        context: grpc.aio.ServicerContext,
    ) -> user_service_pb2.UserResponse:
        print("new user", request.user)
        new_name = request.user.name + "new-name"
        return user_service_pb2.UserResponse(name=new_name)
