import uuid
from typing import Any

from argon2 import PasswordHasher
from starlette.requests import Request

from core.databases.sql.db_helper import db_helper
from core.databases.sql.models import (
    Address,
    Department,
    Audience,
    Group,
    Lesson,
    LessonType,
    GroupSchedule,
    GroupWithNumber,
    PersonalSchedule,
    ScheduleException,
    StudentGroup,
    Specialization,
    TeacherSchedule,
    Student,
    Base,
    Teacher,
    Administrator,
)

from sqladmin import ModelView

from core.databases.sql.models.enums.form_of_education import (
    FormOfEducationEnum,
)
from core.databases.sql.models.enums.type_of_refund import (
    TypeOfRefundEnum,
)


def get_user_form():
    return [
        "first_name",
        "last_name",
        "patronymic",
        "is_active",
        "email",
        "gender",
        "date_of_birth",
    ]


class HashingPasswordMixin:
    column_details_exclude_list = ["password"]
    form_excluded_columns = [
        "id",
        "type",
    ]

    async def on_model_change(
        self,
        data: dict,
        model: Base,
        is_created: bool,
        request: Request,
    ):
        if is_created and (password := data.get("password")):
            ph = PasswordHasher()
            hashed_password = ph.hash(password).encode()
            data["password"] = hashed_password
        return await super().on_model_change(
            data, model, is_created, request
        )


class AdministratorAdmin(
    HashingPasswordMixin,
    ModelView,
    model=Administrator,
):
    form_edit_rules = get_user_form()


class TeacherAdmin(
    HashingPasswordMixin,
    ModelView,
    model=Teacher,
):
    form_edit_rules = get_user_form() + [
        "is_eldest",
        "rank",
        "degree",
        "department",
        "schedules",
    ]


class StudentAdmin(
    HashingPasswordMixin,
    ModelView,
    model=Student,
):
    form_edit_rules = get_user_form() + [
        "personal_number",
        "schedules",
        "schedule_exceptions",
        "groups",
    ]


class AddressAdmin(ModelView, model=Address):
    column_list = "__all__"


class AudienceAdmin(ModelView, model=Audience):
    column_list = [Audience.name, Audience.address]
    column_details_list = [Audience.name, Audience.address]
    form_columns = [Audience.name, Audience.address]


class DepartmentAdmin(ModelView, model=Department):
    column_list = [Department.name]


class GroupAdmin(ModelView, model=Group):
    column_list = "__all__"


class GroupWithNumberAdmin(ModelView, model=GroupWithNumber):
    column_list = "__all__"


class LessonAdmin(ModelView, model=Lesson):
    column_list = [Lesson.name, Lesson.department]
    column_details_list = [
        Lesson.name,
        Lesson.on_schedule,
        Lesson.department,
    ]

    form_columns = [
        Lesson.name,
        Lesson.on_schedule,
        Lesson.department,
    ]


class LessonTypeAdmin(ModelView, model=LessonType):
    column_list = "__all__"


class GroupScheduleAdmin(ModelView, model=GroupSchedule):
    column_list = [
        "id",
        "group_id",
        "lesson",
        "group",
        "number",
        "date",
        "type_of_lesson",
    ]
    form_excluded_columns = ["id", "type"]


class PersonalScheduleAdmin(ModelView, model=PersonalSchedule):
    column_list = "__all__"


class ScheduleExceptionAdmin(ModelView, model=ScheduleException):
    column_list = "__all__"


class UserGroupAdmin(ModelView, model=StudentGroup):
    column_list = "__all__"

    async def insert_model(
        self, request: Request, data: dict
    ) -> Any:
        async with (
            db_helper.get_async_session_with_commit() as session
        ):
            student_id = uuid.UUID(data["student"])
            group_id = uuid.UUID(data["group"])

            obj = StudentGroup(
                student_id=student_id,
                group_id=group_id,
                form_of_education=FormOfEducationEnum[
                    data["form_of_education"]
                ],
                type_of_refund=TypeOfRefundEnum[
                    data["type_of_refund"]
                ],
                is_prefect=data["is_prefect"],
            )
            session.add(obj)
        return obj


class SpecializationAdmin(ModelView, model=Specialization):
    column_list = "__all__"


class TeacherScheduleAdmin(ModelView, model=TeacherSchedule):
    column_list = "__all__"
