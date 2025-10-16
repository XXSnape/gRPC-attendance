from core.databases.sql.models import (
    Administrator,
    Student,
    Teacher,
    User,
)

from .base import BaseDAO


class UserDAO(BaseDAO):
    model = User


class StudentDAO(BaseDAO):
    model = Student


class TeacherDAO(BaseDAO):
    model = Teacher


class AdministratorDAO(BaseDAO):
    model = Administrator
