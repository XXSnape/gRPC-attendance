from core.databases.sql.dao.teacher_schedule import (
    TeacherScheduleDAO,
)

from .base import BaseService


class TeacherService(BaseService):
    dao_class = TeacherScheduleDAO
