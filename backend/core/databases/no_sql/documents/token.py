import datetime
import uuid
from typing import Literal

from beanie import Document, Indexed
from core import settings
from pydantic import Field
from pymongo import ASCENDING, IndexModel


def generate_utc_dt():
    return datetime.datetime.now(datetime.UTC)


class Token(Document):
    created_at: datetime.datetime = Field(
        default_factory=generate_utc_dt
    )
    token: Indexed(str, unique=True)
    full_name: str
    user_id: uuid.UUID
    type: Literal[
        "student",
        "teacher",
        "administrator",
    ]

    class Settings:
        name = "tokens"
        indexes = [
            IndexModel(
                [("created_at", ASCENDING)],
                expireAfterSeconds=settings.auth.token_duration,
            ),
        ]

