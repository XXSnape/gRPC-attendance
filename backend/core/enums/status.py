from enum import IntEnum, auto


class AttendanceStatus(IntEnum):
    PRESENT = auto()
    ABSENT = auto()
    SKIP_RESPECTFULLY = auto()
