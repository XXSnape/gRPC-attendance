import uuid

from core.databases.sql.models import Schedule, TeacherSchedule
from sqlalchemy import extract, select

from .protocols.schedule import ScheduleProtocol


class TeacherScheduleDAO(ScheduleProtocol):
    model = TeacherSchedule

    async def get_user_lessons_for_month(
        self,
        month: int,
        year: int,
        user_id: uuid.UUID,
    ):
        query = (
            select(Schedule.date.distinct())
            .join(
                TeacherSchedule,
            )
            .where(
                extract("YEAR", Schedule.date) == year,
                extract("MONTH", Schedule.date) == month,
                TeacherSchedule.teacher_id == user_id,
            )
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())
