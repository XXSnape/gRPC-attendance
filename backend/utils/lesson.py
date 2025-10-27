from core.grpc.pb import lesson_service_pb2
from core.schemas import lesson


async def create_attendances(
    attendance_data: list[lesson.MarkStudentAttendanceSchema],
):
    for attendance in attendance_data:

        request = lesson_service_pb2.StudentAttendanceRequest(
            **attendance.model_dump(mode="json"),
        )
        yield request
