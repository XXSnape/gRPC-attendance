import asyncio
import datetime

from argon2 import PasswordHasher
from loguru import logger

from core.databases.sql.dao.user import AdministratorDAO
from core.databases.sql.db_helper import db_helper
from core.databases.sql.models.enums.gender import GenderEnum
from core.schemas.user import (
    BaseUserSchema,
    HashedPasswordUserSchema,
)


async def create_admin(user: BaseUserSchema):
    async with db_helper.get_async_session_with_commit() as session:
        dao = AdministratorDAO(session=session)
        ph = PasswordHasher()
        hashed_password = ph.hash(user.password).encode()
        hashed_user_data = HashedPasswordUserSchema(
            **user.model_dump(exclude={"password"}),
            password=hashed_password,
        )
        await dao.add(hashed_user_data)
        logger.success(f"Администратор {user.email} создан.")


if __name__ == "__main__":
    user_data = BaseUserSchema(
        first_name="Admin",
        last_name="Admin",
        patronymic="Admin",
        password="admin",
        is_active=True,
        email="admin@example.com",
        gender=GenderEnum.MALE,
        date_of_birth=datetime.datetime(2000, 1, 1),
        type="administrator",
    )
    asyncio.run(create_admin(user_data))
