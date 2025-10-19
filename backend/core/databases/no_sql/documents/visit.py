import uuid
from core.enums.status import AttendanceStatus


from beanie import Document
from pymongo import IndexModel, ASCENDING


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
