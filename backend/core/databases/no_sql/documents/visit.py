import uuid
from core.enums.status import AttendanceStatus


from beanie import Document
from pymongo import IndexModel, ASCENDING


class Visit(Document):

    user_id: uuid.UUID
    status: AttendanceStatus
    lesson_id: uuid.UUID


    class Settings:
        name = "visits"
        indexes = [
            IndexModel(
                [("user_id", ASCENDING), ("lesson_id", ASCENDING)],
                unique=True,
                name="user_lesson_unique"
            ),
        ]

