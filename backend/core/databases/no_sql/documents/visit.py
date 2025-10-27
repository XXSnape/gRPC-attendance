import uuid

from beanie import Document
from core.enums.status import AttendanceStatus
from pymongo import ASCENDING, IndexModel


class Visit(Document):

    student_id: uuid.UUID
    status: AttendanceStatus
    schedule_id: uuid.UUID


    class Settings:
        name = "visits"
        indexes = [
            IndexModel(
                [("student_id", ASCENDING), ("schedule_id", ASCENDING)],
                unique=True,
                name="user_lesson_unique"
            ),
        ]
