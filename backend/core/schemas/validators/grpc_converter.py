from google.protobuf.message import Message
from pydantic import BeforeValidator


def convert_empty_grpc_to_none[V](value: V) -> V | None:
    if not isinstance(value, Message):
        return value
    if not value.ListFields():
        return None
    return value


gRPCValidator = BeforeValidator(convert_empty_grpc_to_none)
