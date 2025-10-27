from typing import Literal

from core.enums.status import AttendanceStatus
from pydantic import computed_field

from .common import BaseSchema


class AttendanceSchema(BaseSchema):
    status: AttendanceStatus = AttendanceStatus.ABSENT

    @computed_field
    @property
    def decryption(self) -> Literal["+", "Н", "У"]:
        match self.status:
            case AttendanceStatus.PRESENT:
                return "+"
            case AttendanceStatus.ABSENT:
                return "Н"
            case AttendanceStatus.SKIP_RESPECTFULLY:
                return "У"
