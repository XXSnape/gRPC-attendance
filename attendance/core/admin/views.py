from core.databases.sql.models import (
    Address,
    Department,
    Audience,
    Group,
    Lesson,
    LessonType,
    GroupSchedule,
    PersonalSchedule,
    ScheduleException,
    StudentGroup,
    Specialization,
    TeacherSchedule,
    Schedule,
)

from sqladmin import ModelView


class AddressAdmin(ModelView, model=Address):
    column_list = "__all__"


class AudienceAdmin(ModelView, model=Audience):
    column_list = "__all__"


class DepartmentAdmin(ModelView, model=Department):
    column_list = "__all__"


class GroupAdmin(ModelView, model=Group):
    column_list = "__all__"


class LessonAdmin(ModelView, model=Lesson):
    column_list = "__all__"


class LessonTypeAdmin(ModelView, model=LessonType):
    column_list = "__all__"


class ScheduleAdmin(ModelView, model=Schedule):
    column_list = "__all__"


class GroupScheduleAdmin(ModelView, model=GroupSchedule):
    column_list = [
        "id",
        "group_id",
        "group",
    ]
    form_columns = ["group_schedule"]


class PersonalScheduleAdmin(ModelView, model=PersonalSchedule):
    column_list = "__all__"


class ScheduleExceptionAdmin(ModelView, model=ScheduleException):
    column_list = "__all__"


class UserGroupAdmin(ModelView, model=StudentGroup):
    column_list = "__all__"


class SpecializationAdmin(ModelView, model=Specialization):
    column_list = "__all__"


class TeacherScheduleAdmin(ModelView, model=TeacherSchedule):
    column_list = "__all__"
