import asyncio
import logging
import os
from uuid import UUID

import grpc

import postservice_pb2
import postservice_pb2_grpc
from repositories.postgres.repository import PostgresPostRepository
from repositories.schemas import PostCreate, PostUpdate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        logger.info(f"Created post: {post}")
        return postservice_pb2.CreatePostResponse(post=post.to_proto())

    async def GetPost(self, request, context):
        post = await self.repo.get(UUID(request.post_id))
        if not post:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Post not found")
            return postservice_pb2.GetPostResponse()

        if post.is_private and post.creator_id != request.requester_id:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Access denied to private post")
            return postservice_pb2.GetPostResponse()

        return postservice_pb2.GetPostResponse(post=post.to_proto())

    async def UpdatePost(self, request, context):
        post = await self.repo.get(UUID(request.post_id))
        if not post:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Post not found")
            return postservice_pb2.UpdatePostResponse()

        if post.creator_id != request.requester_id:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("You are not the owner of the post")
            return postservice_pb2.UpdatePostResponse()

        post_update = PostUpdate(
            title=request.title if request.title else None,
            description=request.description if request.description else None,
            is_private=request.is_private,
            tags=list(request.tags) if request.tags else None
        )

        updated_post = await self.repo.update(UUID(request.post_id), post_update)
        if not updated_post:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to update post")
            return postservice_pb2.UpdatePostResponse()

        return postservice_pb2.UpdatePostResponse(post=updated_post.to_proto())

    async def DeletePost(self, request, context):
        post = await self.repo.get(UUID(request.post_id))
        if not post:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Post not found")
            return postservice_pb2.DeletePostResponse(success=False)

        if post.creator_id != request.requester_id:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("You are not the owner of the post")
            return postservice_pb2.DeletePostResponse(success=False)

        success = await self.repo.delete(UUID(request.post_id))
        return postservice_pb2.DeletePostResponse(success=success)

    async def ListPosts(self, request, context):
        offset = (request.page - 1) * request.page_size
        limit = request.page_size
        posts, total_count = await self.repo.list_posts(
            creator_id=request.creator_id,
            offset=offset,
            limit=limit
        )

        if request.creator_id != request.requester_id:
            public_posts = [post.to_proto() for post in posts if post.is_private == False]
            return postservice_pb2.ListPostsResponse(
                posts=public_posts,
                total_count=len(public_posts)
            )

        return postservice_pb2.ListPostsResponse(
            posts=[post.to_proto() for post in posts],
            total_count=total_count
        )


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
