import asyncio

import grpc
from beanie import init_beanie
from core.config import settings
from core.databases.no_sql import documents
from core.grpc.implementations.lesson import LessonServiceServicer
from core.grpc.implementations.user import UserServiceServicer
from core.grpc.pb import (
    lesson_service_pb2_grpc,
    user_service_pb2_grpc,
)
from loguru import logger
from pymongo import AsyncMongoClient


async def main():
    server = grpc.aio.server()
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(), server
    )
    lesson_service_pb2_grpc.add_LessonServiceServicer_to_server(
        LessonServiceServicer(), server
    )

    server.add_insecure_port(f"[::]:{settings.run.grpc_server_port}")
    client = AsyncMongoClient(str(settings.mongo_db.url))
    try:
        await init_beanie(
            database=client.db_name,
            document_models=[
                documents.Token,
                documents.Visit,
                documents.AccessForPrefects,
                documents.TrackingAttendance,
                documents.QRCode,
            ],
        )
        await server.start()
        logger.success(
            "Listening on port :{}", settings.run.grpc_server_port
        )
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.shutdown()
        await client.close()
        logger.success("Received keyboard interrupt, shutting down")


if __name__ == "__main__":
    asyncio.run(main())
