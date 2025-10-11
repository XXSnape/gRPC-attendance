import uuid

from pydantic import BaseModel


class IdSchema(BaseModel):
    id: uuid.UUID
