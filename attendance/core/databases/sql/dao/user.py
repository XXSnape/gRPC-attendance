from .base import BaseDAO
from core.databases.sql.models import Student, Teacher, Administrator


class StudentDAO(BaseDAO):
    model = Student


class TeacherDAO(BaseDAO):
    model = Teacher


class AdministratorDAO(BaseDAO):
    model = Administrator
