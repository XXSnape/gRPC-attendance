import datetime
import uuid

from beanie import Document
from pydantic import Field

from .utils.dt import generate_utc_dt
from core.enums.status import AttendanceStatus


class TrackingAttendance(Document):
    student_id: uuid.UUID
    schedule_id: uuid.UUID
    user_id_changed_status: uuid.UUID
    status: AttendanceStatus
    date_and_time_of_change: datetime.datetime = Field(
        default_factory=generate_utc_dt
    )
