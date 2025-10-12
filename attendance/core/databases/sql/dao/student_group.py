from .base import BaseDAO
from core.databases.sql.models import StudentGroup


class StudentGroupDAO(BaseDAO):
    model = StudentGroup
