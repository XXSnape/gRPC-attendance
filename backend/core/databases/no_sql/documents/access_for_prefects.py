import datetime
import uuid

from beanie import Document, before_event, Insert
from pydantic import Field

from .utils.dt import generate_utc_dt


class AccessForPrefects(Document):
    user_id_guaranteed_access: uuid.UUID
    schedule_id: uuid.UUID
    group_id: uuid.UUID
    number_of_minutes_of_access: int
    access_start_date_and_time: datetime.datetime = Field(
        default_factory=generate_utc_dt,
    )
    date_and_time_of_access_closure: datetime.datetime | None = None
    date_and_time_of_forced_access_closure: (
        datetime.datetime | None
    ) = None

    @before_event(Insert)
    def convert_date_and_time_of_end_of_access(self):
        self.date_and_time_of_access_closure = (
            self.access_start_date_and_time
            + datetime.timedelta(
                minutes=self.number_of_minutes_of_access,
            )
        )
