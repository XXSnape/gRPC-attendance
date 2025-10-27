from core.databases.sql.dao.group_schedule import GroupScheduleDAO

from .base import BaseService


class StudentService(BaseService):
    dao_class = GroupScheduleDAO
