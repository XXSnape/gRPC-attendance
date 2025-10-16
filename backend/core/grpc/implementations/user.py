import secrets

import grpc
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from core import settings
from core.databases.no_sql.documents import Token
from core.databases.sql.dao.user import UserDAO
from core.databases.sql.db_helper import db_helper
from core.grpc.pb import user_pb2, user_service_pb2, user_service_pb2_grpc
from core.schemas.user import UserEmailSchema


class UserServiceServicer(
    user_service_pb2_grpc.UserServiceServicer,
):
    async def UserSingIn(
        self,
        request: user_service_pb2.SingInRequest,
        context: grpc.aio.ServicerContext,
    ) -> user_service_pb2.SingInResponse:
        error = "Неверный логин или пароль"
        async with (
            db_helper.get_async_session_without_commit() as session
        ):
            dao = UserDAO(session)
            user = await dao.find_one_or_none(
                UserEmailSchema(email=request.email)
            )
            if not user:
                await context.abort(
                    grpc.StatusCode.NOT_FOUND,
                    details=error,
                )
            ph = PasswordHasher()
            try:
                ph.verify(user.password, request.password)
            except VerifyMismatchError:
                await context.abort(
                    grpc.StatusCode.NOT_FOUND,
                    details=error,
                )
            token = secrets.token_urlsafe(settings.auth.token_length)
            document = await Token.insert_one(
                Token(
                    token=token,
                    user_id=user.id,
                    full_name=user.full_name,
                    type=user.type,
                )
            )
            return user_service_pb2.SingInResponse(
                token=document.token,
                user=user_pb2.UserData(
                    type=document.type,
                    full_name=document.full_name,
                    id=str(document.user_id),
                ),
            )

    async def UserAuth(
        self,
        request: user_service_pb2.AuthRequest,
        context: grpc.aio.ServicerContext,
    ) -> user_pb2.UserData:
        error = "Пользователь не авторизован"
        metadata = dict(context.invocation_metadata())
        token = metadata.get("authorization")
        if not token:
            await context.abort(
                grpc.StatusCode.UNAUTHENTICATED,
                details=error,
            )
        token_document = await Token.find_one(Token.token == token)
        if not token_document:
            await context.abort(
                grpc.StatusCode.UNAUTHENTICATED,
                details=error,
            )
        return user_pb2.UserData(
            id=str(token_document.user_id),
            type=token_document.type,
            full_name=token_document.full_name,
        )
