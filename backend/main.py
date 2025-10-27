from contextlib import asynccontextmanager

import grpc
from api import router as api_router
from core import settings
from core.admin import views as admin_views
from core.databases.sql.db_helper import db_helper
from core.grpc.pb import (
    lesson_service_pb2_grpc,
    user_service_pb2_grpc,
)
from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with grpc.aio.insecure_channel(
        settings.run.grpc_url
    ) as channel:
        user_stub = user_service_pb2_grpc.UserServiceStub(channel)
        lesson_stub = lesson_service_pb2_grpc.LessonServiceStub(
            channel
        )
        app.state.user_stub = user_stub
        app.state.lesson_stub = lesson_stub
        yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

views = [
    admin_views.AddressAdmin,
    admin_views.AudienceAdmin,
    admin_views.DepartmentAdmin,
    admin_views.GroupAdmin,
    admin_views.GroupWithNumberAdmin,
    admin_views.LessonAdmin,
    admin_views.LessonTypeAdmin,
    admin_views.GroupScheduleAdmin,
    admin_views.ScheduleExceptionAdmin,
    admin_views.UserGroupAdmin,
    admin_views.SpecializationAdmin,
    admin_views.TeacherScheduleAdmin,
    admin_views.StudentAdmin,
    admin_views.TeacherAdmin,
    admin_views.AdministratorAdmin,
    admin_views.ScheduleAdmin,
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
