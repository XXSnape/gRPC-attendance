import datetime
import uuid
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

import grpc
from beanie.odm.operators.update.general import Set

from core.databases.no_sql.documents import Visit, TrackingAttendance
from core.databases.sql.dao.group_schedule import GroupScheduleDAO
from core.databases.sql.dao.protocols.schedule import (
    ScheduleProtocol,
)
from core.databases.sql.models import Schedule
from core.grpc.pb import lesson_service_pb2, lesson_pb2
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.attendance import AttendanceSchema
from core.schemas.lesson import (
    GroupSchema,
)
from core.schemas.user import UserAttendanceSchema


class BaseService(ABC):
    dao_class: type[ScheduleProtocol]
    can_t_view_lesson_details: str

    def __init__(self, session: AsyncSession | None = None):
        self._session: AsyncSession | None = session

    async def get_user_lessons_for_month(
        self,
        month: int,
        year: int,
        user_id: uuid.UUID,
    ):
        dates = await self.dao_class(
            self._session
        ).get_user_lessons_for_month(
            month,
            year,
            user_id,
        )
        return lesson_service_pb2.LessonsForMonthResponse(
            dates=[str(date) for date in dates]
        )

    @abstractmethod
    async def get_schedule_by_date(
        self,
        date: datetime.date,
        user_id: uuid.UUID,
    ) -> lesson_service_pb2.LessonsResponse: ...

    @abstractmethod
    async def get_lesson_details(
        self,
        user_id: uuid.UUID,
        schedule_id: uuid.UUID,
        context: grpc.aio.ServicerContext,
    ) -> lesson_service_pb2.LessonDetailsResponse: ...

    @abstractmethod
    async def check_for_access(
        self,
        user_id: uuid.UUID,
        schedule_id: uuid.UUID,
        group_id: uuid.UUID,
        context: grpc.aio.ServicerContext,
    ) -> None: ...

    async def get_schedule_and_groups(
        self,
        schedule_id: uuid.UUID,
        user_id: uuid.UUID,
        context: grpc.aio.ServicerContext,
    ) -> tuple[Schedule, list[GroupSchema]]:
        dao_obj = self.dao_class(self._session)
        schedule = await dao_obj.get_lesson_details(
            user_id=user_id,
            schedule_id=schedule_id,
        )
        if schedule is None:
            await context.abort(
                grpc.StatusCode.NOT_FOUND,
                self.can_t_view_lesson_details,
            )
        groups = []
        documents = await Visit.find(
            Visit.schedule_id == schedule_id
        ).to_list()
        for group_with_number in schedule.groups_with_numbers:
            group_schema = GroupSchema(
                id=group_with_number.id,
                complete_name=group_with_number.complete_name,
                attendances=[],
            )
            groups.append(group_schema)
            group_attendances = []
            for (
                student_with_group
            ) in group_with_number.students_with_groups:
                schema = UserAttendanceSchema(
                    full_name=student_with_group.student.full_name,
                    decryption_of_full_name=student_with_group.student.decryption_of_full_name,
                    personal_number=student_with_group.student.personal_number,
                    is_prefect=student_with_group.is_prefect,
                    student_id=student_with_group.student_id,
                )
                for document in documents:
                    if (
                        document.student_id
                        == student_with_group.student_id
                    ):
                        schema.attendance.status = document.status
                        break
                group_attendances.append(schema)
            group_schema.attendances = group_attendances
        schedule.can_be_edited_by_prefect = False
        schedule.total_attendance = None
        schedule.group_names = [
            group.complete_name for group in groups
        ]
        return schedule, groups

    async def set_students_attendance(
        self,
        user_id: uuid.UUID,
        schedule_id: uuid.UUID,
        group_id: uuid.UUID,
        context: grpc.aio.ServicerContext,
        request_iterator: AsyncIterator[
            lesson_service_pb2.StudentAttendanceRequest
        ],
    ) -> AsyncIterator[lesson_service_pb2.StudentAttendanceResponse]:
        await self.check_for_access(
            user_id=user_id,
            schedule_id=schedule_id,
            group_id=group_id,
            context=context,
        )
        dao = GroupScheduleDAO(session=self._session)

        groups_with_numbers = await dao.get_students_of_group(
            schedule_id=schedule_id,
            group_id=group_id,
        )
        if groups_with_numbers is None:
            await context.abort(
                grpc.StatusCode.NOT_FOUND,
                "Расписание для указанной группы не найдено.",
            )
            return
        students_ids = [
            swg.student_id
            for swg in groups_with_numbers.students_with_groups
        ]

        async for request in request_iterator:
            student_id_uuid = uuid.UUID(request.student_id)
            if student_id_uuid in students_ids:
                await Visit.find_one(
                    Visit.schedule_id == schedule_id,
                    Visit.student_id == request.student_id,
                ).upsert(
                    Set({Visit.status: request.attendance.status}),
                    on_insert=Visit(schedule_id=schedule_id),
                    student_id=student_id_uuid,
                    status=request.attendance.status,
                )
                await TrackingAttendance(
                    student_id=student_id_uuid,
                    schedule_id=schedule_id,
                    user_id_changed_status=user_id,
                    status=request.attendance.status,
                ).insert()

                yield lesson_service_pb2.StudentAttendanceResponse(
                    student_id=request.student_id,
                    attendance=lesson_pb2.Attendance(
                        **AttendanceSchema(
                            status=request.attendance.status
                        ).model_dump(mode="json")
                    ),
                )
