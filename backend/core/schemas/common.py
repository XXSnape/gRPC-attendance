import uuid
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    BeforeValidator,
)


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IdSchema(BaseSchema):
    id: Annotated[
        uuid.UUID,
        BeforeValidator(
            lambda v: uuid.UUID(v) if isinstance(v, str) else v
        ),
    ]
