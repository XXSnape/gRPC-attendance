import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, PlainSerializer


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IdSchema(BaseSchema):
    id: Annotated[uuid.UUID | str, PlainSerializer(lambda v: str(v))]
