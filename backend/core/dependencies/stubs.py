from typing import Annotated, Any, TypeAlias

from core.grpc.pb.lesson_service_pb2_grpc import LessonServiceStub
from core.grpc.pb.user_service_pb2_grpc import UserServiceStub
from fastapi import Depends, Request


def get_stub(name: str):
    def _get_stub(request: Request) -> Any:
        return getattr(request.app.state, name)

    return _get_stub


UserStub: TypeAlias = Annotated[
    UserServiceStub,
    Depends(get_stub(name="user_stub")),
]
LessonStub: TypeAlias = Annotated[
    LessonServiceStub, Depends(get_stub(name="lesson_stub"))
]
