from contextlib import asynccontextmanager
from typing import Literal, Annotated

import grpc
from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from core import settings
from core.grpc.pb import user_service_pb2, user_pb2
from core.grpc.pb import user_service_pb2_grpc
from api import router as api_router

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

# class User(BaseModel):
#     name: str
#     age: int
#     sex: Literal["MALE", "FEMALE"]
#
#
# def get_stab(request: Request):
#     return request.app.state.stub
#
#
# @app.get("/form")
# async def login_page(request: Request):
#     return templates.TemplateResponse(
#         "user.html", {"request": request}
#     )
#
#
# @app.post("/submit")
# async def submit_form(
#     request: Request,
#     user_data: Annotated[User, Form()],
#     stab: Annotated[
#         user_service_pb2_grpc.UserServiceStub, Depends(get_stab)
#     ],
# ):
#     print("stab", stab)
#     req = user_service_pb2.NewUserRequest(
#         user=user_pb2.User(
#             name=user_data.name, age=user_data.age, sex=user_data.sex
#         )
#     )
#     print("req", req)
#     response = await stab.CreateUser(req)
#     print("resp", response)
#     print("name", response.name)
#     return templates.TemplateResponse(
#         "user.html", {"request": request, "new_name": response.name}
#     )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
