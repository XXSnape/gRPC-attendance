from contextlib import asynccontextmanager

import grpc
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from sqladmin import Admin

from core import settings
from core.databases.sql.db_helper import db_helper
from core.grpc.pb import user_service_pb2_grpc
from api import router as api_router
from core.admin import views as admin_views

templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with grpc.aio.insecure_channel(
        settings.run.grpc_url
    ) as channel:
        user_stub = user_service_pb2_grpc.UserServiceStub(channel)
        app.state.user_stub = user_stub
        yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


views = [
    admin_views.AddressAdmin,
    admin_views.AudienceAdmin,
    admin_views.DepartmentAdmin,
    admin_views.GroupAdmin,
    admin_views.GroupWithNumberAdmin,
    admin_views.LessonAdmin,
    admin_views.LessonTypeAdmin,
    admin_views.GroupScheduleAdmin,
    admin_views.PersonalScheduleAdmin,
    admin_views.ScheduleExceptionAdmin,
    admin_views.UserGroupAdmin,
    admin_views.SpecializationAdmin,
    admin_views.TeacherScheduleAdmin,
    admin_views.StudentAdmin,
    admin_views.TeacherAdmin,
    admin_views.AdministratorAdmin,
]

admin = Admin(
    app,
    db_helper.engine,
)

for view in views:
    admin.add_view(view)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
