import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from uuid import UUID

import grpc
from aiokafka import AIOKafkaProducer

import postservice_pb2
import postservice_pb2_grpc
from repositories.postgres.repository import PostgresPostRepository, PostgresCommentRepository
from repositories.schemas import PostCreate, PostUpdate, CommentCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostServiceServicer(postservice_pb2_grpc.PostServiceServicer):
    def __init__(
            self,
            post_repo: PostgresPostRepository,
            comment_repo: PostgresCommentRepository,
            kafka_producer: AIOKafkaProducer
    ):
        self.post_repo = post_repo
        self.comment_repo = comment_repo
        self.producer = kafka_producer

    async def CreatePost(self, request, context):
        post = await self.post_repo.create(PostCreate(
            title=request.title,
            description=request.description,
            creator_id=request.creator_id,
            is_private=request.is_private,
            tags=request.tags
        ))
        logger.info(f"Created post: {post}")
        return postservice_pb2.CreatePostResponse(post=post.to_proto())

    async def GetPost(self, request, context):
        post = await self.post_repo.get(UUID(request.post_id))
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
        post = await self.post_repo.get(UUID(request.post_id))
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

        updated_post = await self.post_repo.update(UUID(request.post_id), post_update)
        if not updated_post:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to update post")
            return postservice_pb2.UpdatePostResponse()

        return postservice_pb2.UpdatePostResponse(post=updated_post.to_proto())

    async def DeletePost(self, request, context):
        post = await self.post_repo.get(UUID(request.post_id))
        if not post:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Post not found")
            return postservice_pb2.DeletePostResponse(success=False)

        if post.creator_id != request.requester_id:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("You are not the owner of the post")
            return postservice_pb2.DeletePostResponse(success=False)

        success = await self.post_repo.delete(UUID(request.post_id))
        return postservice_pb2.DeletePostResponse(success=success)

    async def ListPosts(self, request, context):
        offset = (request.page - 1) * request.page_size
        limit = request.page_size
        posts, total_count = await self.post_repo.list_posts(
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

    async def ViewPost(self, request, context):
        event = {
            "post_id": request.post_id,
            "viewer_id": request.viewer_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await self.producer.send_and_wait(
            "post_views",
            json.dumps(event, ensure_ascii=False).encode("utf-8")
        )
        await self.post_repo.view(UUID(request.post_id))
        return postservice_pb2.ViewPostResponse(success=True)

    async def LikePost(self, request, context):
        event = {
            "post_id": request.post_id,
            "user_id": request.user_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await self.producer.send_and_wait(
            "post_likes",
            json.dumps(event, ensure_ascii=False).encode("utf-8")
        )
        await self.post_repo.like(UUID(request.post_id))
        return postservice_pb2.LikePostResponse(success=True)

    async def AddComment(self, request, context):
        comment = await self.comment_repo.create(CommentCreate(
            post_id=UUID(request.post_id),
            user_id=request.user_id,
            text=request.text,
        ))
        event = {
            "comment_id": str(comment.id),
            "post_id": request.post_id,
            "user_id": request.user_id,
            "text": comment.text,
            "timestamp": comment.created_at.isoformat()
        }
        await self.producer.send_and_wait(
            "post_comments",
            json.dumps(event, ensure_ascii=False).encode("utf-8")
        )
        return postservice_pb2.AddCommentResponse(comment=comment.to_proto())

    async def GetComments(self, request, context):
        offset = (request.page - 1) * request.page_size
        limit = request.page_size
        comments, total_count = await self.comment_repo.list_comments(
            post_id=request.post_id,
            offset=offset,
            limit=limit
        )

        return postservice_pb2.GetCommentsResponse(
            comments=[comment.to_proto() for comment in comments],
            total_count=total_count
        )


async def serve():
    server = grpc.aio.server()
    dns = os.getenv("DB_DNS", "postgresql+asyncpg://postgres:postgres@localhost/postgres")

    post_repo = PostgresPostRepository(dns)
    await post_repo.create_tables()

    comment_repo = PostgresCommentRepository(dns)
    await comment_repo.create_tables()

    while True:
        try:
            producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
            await producer.start()
            break
        except Exception:
            await asyncio.sleep(1)

    postservice_pb2_grpc.add_PostServiceServicer_to_server(
        PostServiceServicer(
            post_repo=post_repo,
            comment_repo=comment_repo,
            kafka_producer=producer,
        ),
        server
    )
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
