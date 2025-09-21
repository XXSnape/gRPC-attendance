import asyncio
from core.pb import user_service_pb2_grpc
from services.user import UserServiceServicer
import grpc
from loguru import logger


async def serve() -> None:
    server = grpc.aio.server()
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    await server.start()
    logger.success("Listening on port :50051")
    await server.wait_for_termination()


async def main():
    server = grpc.aio.server()
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    try:
        await server.start()
        logger.success("Listening on port :50051")
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.shutdown()
        print("Received keyboard interrupt, shutting down")


if __name__ == "__main__":
    asyncio.run(main())
