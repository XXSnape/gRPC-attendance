from core.databases.sql.models import StudentGroup

from .base import BaseDAO


class StudentGroupDAO(BaseDAO):
    model = StudentGroup
