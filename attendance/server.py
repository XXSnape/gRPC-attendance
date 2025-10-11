import asyncio
from core.grpc.pb import user_service_pb2_grpc
from core.grpc.implementations.user import UserServiceServicer

import grpc
from loguru import logger
from core.config import settings


async def main():
    server = grpc.aio.server()
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(), server
    )
    server.add_insecure_port(f"[::]:{settings.run.grpc_server_port}")
    try:
        await server.start()
        logger.success(
            "Listening on port :{}", settings.run.grpc_server_port
        )
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.shutdown()
        logger.success("Received keyboard interrupt, shutting down")


if __name__ == "__main__":
    asyncio.run(main())
