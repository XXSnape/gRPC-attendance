from .base import BaseDAO
from core.databases.sql.models import (
    User,
    Student,
    Teacher,
    Administrator,
)


class UserDAO(BaseDAO):
    model = User


class StudentDAO(BaseDAO):
    model = Student


class TeacherDAO(BaseDAO):
    model = Teacher


class AdministratorDAO(BaseDAO):
    model = Administrator
