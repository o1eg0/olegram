import asyncio
import os

import grpc

import postservice_pb2
import postservice_pb2_grpc
from repositories.postgres.repository import PostgresPostRepository
from repositories.schemas import PostCreate


class PostServiceServicer(postservice_pb2_grpc.PostServiceServicer):
    def __init__(self, repository: PostgresPostRepository):
        self.repo = repository

    async def CreatePost(self, request, context):
        post = await self.repo.create(PostCreate(
            title=request.title,
            description=request.description,
            creator_id=request.creator_id,
            is_private=request.is_private,
            tags=request.tags
        ))
        return postservice_pb2.CreatePostResponse(post=postservice_pb2.Post(**post.model_dump()))



async def serve():
    server = grpc.aio.server()
    dns = os.getenv("DB_DNS", "postgresql+asyncpg://postgres:postgres@localhost/postgres")
    repo = PostgresPostRepository(dns)
    await repo.create_tables()
    postservice_pb2_grpc.add_PostServiceServicer_to_server(PostServiceServicer(repo), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
