import uuid

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.databases.sql.models import StudentGroup, GroupWithNumber

from .base import BaseDAO


class StudentGroupDAO(BaseDAO):
    model = StudentGroup

    async def get_group_by_student_id(self, user_id: uuid.UUID):
        query = (
            select(self.model)
            .where(
                self.model.student_id == user_id,
                # self.model.is_prefect.is_(True),
            )
            .options(
                joinedload(StudentGroup.group).selectinload(
                    GroupWithNumber.students
                )
            )
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()
