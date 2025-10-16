import asyncio
from core.databases.no_sql import documents

from beanie import init_beanie
from pymongo import AsyncMongoClient

from core.grpc.implementations.lesson import LessonServiceServicer
from core.grpc.pb import (
    user_service_pb2_grpc,
    lesson_service_pb2_grpc,
)
from core.grpc.implementations.user import UserServiceServicer

import grpc
from loguru import logger
from core.config import settings


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
