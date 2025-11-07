import datetime
import uuid

from beanie import Document, Indexed
from core import settings
from pydantic import Field
from pymongo import ASCENDING, IndexModel
from utils.dt import generate_utc_dt


class QRCode(Document):
    schedule_id: uuid.UUID
    token: Indexed(str, unique=True)
    created_at: datetime.datetime = Field(
        default_factory=generate_utc_dt
    )

    class Settings:
        indexes = [
            IndexModel(
                [("created_at", ASCENDING)],
                expireAfterSeconds=settings.app.validity_period_of_qr_code,
            ),
        ]
