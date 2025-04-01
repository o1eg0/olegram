import os
from typing import Annotated

import grpc
import httpx
from fastapi import FastAPI, Request, HTTPException, Depends, APIRouter, Header

from schemas import Post, PostCreate, PostUpdate, PostList
import postservice_pb2
from postservice_pb2_grpc import PostServiceStub

app = FastAPI(title="API Gateway")

USER_SERVICE_URL = os.getenv("USER_SERVICE_ADDR")
POST_COMMENT_ADDR = os.getenv("POST_COMMENT_ADDR")

grpc_channel = grpc.aio.insecure_channel(POST_COMMENT_ADDR)
post_service_stub = PostServiceStub(grpc_channel)


async def get_current_user(jwt_token: Annotated[str, Header()]) -> str | None:
    if not jwt_token:
        raise HTTPException(401, detail="Unauthorized")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://{USER_SERVICE_URL}/validate",
            headers={"jwt-token": jwt_token}
        )
    data = response.json()
    if response.status_code != 200 or data.get("status") != "success":
        raise HTTPException(401, detail="Invalid token")
    return data.get("username", None)


@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"], tags=["Users"])
async def proxy_users(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"http://{USER_SERVICE_URL}/{path}",
            params=request.query_params,
            content=await request.body(),
            headers=request.headers.raw
        )
    return response.json()


router = APIRouter()


@router.post("/posts", response_model=Post)
async def create_post(
    post: PostCreate,
    username: Annotated[str, Depends(get_current_user)]
):
    grpc_request = postservice_pb2.CreatePostRequest(
        title=post.title,
        description=post.description,
        creator_id=username,  # прокидываем ID пользователя
        is_private=post.is_private,
        tags=post.tags
    )

    response = await post_service_stub.CreatePost(grpc_request)
    return Post(
        id=response.post.id,
        title=response.post.title,
        description=response.post.description,
        creator_id=response.post.creator_id,
        created_at=response.post.created_at,
        updated_at=response.post.updated_at,
        is_private=response.post.is_private,
        tags=response.post.tags
    )


@router.get("/posts/{post_id}", response_model=Post)
async def get_post(
    post_id: str,
    username: Annotated[str, Depends(get_current_user)]
):
    grpc_request = postservice_pb2.GetPostRequest(
        post_id=post_id,
        requester_id=username
    )

    response = await post_service_stub.GetPost(grpc_request)
    return Post(
        id=response.post.id,
        title=response.post.title,
        description=response.post.description,
        creator_id=response.post.creator_id,
        created_at=response.post.created_at,
        updated_at=response.post.updated_at,
        is_private=response.post.is_private,
        tags=response.post.tags
    )


@router.put("/posts/{post_id}", response_model=Post)
async def update_post(
        post_id: str,
        post_update: PostUpdate,
        username: Annotated[str, Depends(get_current_user)]
):
    grpc_request = postservice_pb2.UpdatePostRequest(
        post_id=post_id,
        requester_id=username,
        title=post_update.title,
        description=post_update.description,
        is_private=post_update.is_private,
        tags=post_update.tags
    )

    response = await post_service_stub.UpdatePost(grpc_request)
    return Post(
        id=response.post.id,
        title=response.post.title,
        description=response.post.description,
        creator_id=response.post.creator_id,
        created_at=response.post.created_at,
        updated_at=response.post.updated_at,
        is_private=response.post.is_private,
        tags=response.post.tags
    )


@router.delete("/posts/{post_id}", response_model=dict)
async def delete_post(
    post_id: str,
    username: Annotated[str, Depends(get_current_user)]
):
    grpc_request = postservice_pb2.DeletePostRequest(
        post_id=post_id,
        requester_id=username
    )

    response = await post_service_stub.DeletePost(grpc_request)
    return {"success": response.success}


@router.get("/posts", response_model=PostList)
async def list_posts(
    username: Annotated[str, Depends(get_current_user)],
    page: int = 1,
    page_size: int = 10,
):
    grpc_request = postservice_pb2.ListPostsRequest(
        requester_id=username,
        page=page,
        page_size=page_size
    )

    response = await post_service_stub.ListPosts(grpc_request)
    posts = [
        Post(
            id=post.id,
            title=post.title,
            description=post.description,
            creator_id=post.creator_id,
            created_at=post.created_at,
            updated_at=post.updated_at,
            is_private=post.is_private,
            tags=post.tags
        )
        for post in response.posts
    ]
    return PostList(posts=posts, total_count=response.total_count)


app.include_router(router, tags=["Posts"])
