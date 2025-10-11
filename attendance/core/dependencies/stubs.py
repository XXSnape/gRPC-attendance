from typing import Annotated, Any, TypeAlias

from fastapi import Request, Depends

from core.grpc.pb.user_service_pb2_grpc import UserServiceStub


def get_stub(name: str):
    def _get_stub(request: Request) -> Any:
        return getattr(request.app.state, name)

    return _get_stub


UserStub: TypeAlias = Annotated[
    UserServiceStub,
    Depends(get_stub(name="user_stub")),
]
