from enum import StrEnum


class AttendanceStatus(StrEnum):
    PRESENT = "+"
    ABSENT = "Н"
    SKIP_RESPECTFULLY = "У"
