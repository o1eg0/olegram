import os
from pprint import pprint
from typing import Annotated
from uuid import UUID

import grpc
import httpx
from fastapi import FastAPI, Request, HTTPException, Depends, APIRouter, Header, Path

import postservice_pb2
from postservice_pb2_grpc import PostServiceStub
import stats_pb2
from stats_pb2_grpc import StatsServiceStub
from schemas import Post, PostCreate, PostUpdate, PostList, Comment, CommentList, Counter, TimelineResponse, TopItem, \
    TimelinePoint

app = FastAPI(title="API Gateway")

USER_SERVICE_URL = os.getenv("USER_SERVICE_ADDR")
POST_COMMENT_ADDR = os.getenv("POST_COMMENT_ADDR")
STATS_ADDR = os.getenv("STATS_SERVICE_ADDR", "stats_service:50051")
stats_channel = grpc.aio.insecure_channel(STATS_ADDR)
stats_stub = StatsServiceStub(stats_channel)

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
        likes=response.post.likes,
        views=response.post.views,
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
    pprint(response.post)
    return Post(
        id=response.post.id,
        title=response.post.title,
        description=response.post.description,
        creator_id=response.post.creator_id,
        created_at=response.post.created_at,
        updated_at=response.post.updated_at,
        likes=response.post.likes,
        views=response.post.views,
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
        likes=response.post.likes,
        views=response.post.views,
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
        creator_id: str,
        page: int = 1,
        page_size: int = 10,
):
    grpc_request = postservice_pb2.ListPostsRequest(
        requester_id=username,
        page=page,
        page_size=page_size,
        creator_id=creator_id,
    )

    response = await post_service_stub.ListPosts(grpc_request)
    pprint(response.posts)

    posts = [
        Post(
            id=post.id,
            title=post.title,
            description=post.description,
            creator_id=post.creator_id,
            created_at=post.created_at,
            updated_at=post.updated_at,
            likes=post.likes,
            views=post.views,
            is_private=post.is_private,
            tags=post.tags
        )
        for post in response.posts
    ]
    return PostList(posts=posts, total_count=response.total_count)


comments_router = APIRouter()


@comments_router.post("/posts/{post_id}/comment")
async def create_comment(
        post_id: str,
        text: str,
        username: Annotated[str, Depends(get_current_user)]
):
    request = postservice_pb2.AddCommentRequest(
        post_id=post_id,
        user_id=username,
        text=text
    )
    response = await post_service_stub.AddComment(request)
    comment = response.comment
    return Comment(
        id=comment.id,
        post_id=comment.post_id,
        user_id=comment.user_id,
        text=comment.text,
        created_at=comment.created_at
    )


@comments_router.get("/posts/{post_id}/comments")
async def get_comments(
        post_id: str,
        username: Annotated[str, Depends(get_current_user)],
        page: int = 1,
        page_size: int = 10,
):
    request = postservice_pb2.GetCommentsRequest(
        post_id=post_id,
        page=page,
        page_size=page_size,
    )
    response = await post_service_stub.GetComments(request)
    comments = [
        Comment(
            id=comment.id,
            post_id=comment.post_id,
            user_id=comment.user_id,
            text=comment.text,
            created_at=comment.created_at
        )
        for comment in response.comments
    ]
    return CommentList(comments=comments, total_count=response.total_count)


actions_router = APIRouter()


@actions_router.post("/posts/{post_id}/like")
async def like_post(
        post_id: str,
        username: Annotated[str, Depends(get_current_user)]
):
    await post_service_stub.LikePost(postservice_pb2.LikePostRequest(
        post_id=post_id,
        user_id=username
    ))
    return {"status": "success"}


@actions_router.post("/posts/{post_id}/view")
async def view_post(
        post_id: str,
        username: Annotated[str, Depends(get_current_user)]
):
    await post_service_stub.ViewPost(postservice_pb2.ViewPostRequest(
        post_id=post_id,
        viewer_id=username
    ))
    return {"status": "success"}


stats_router = APIRouter(prefix="/stats")


@stats_router.get("/posts/{post_id}", response_model=Counter)
async def post_counters(post_id: UUID):
    resp = await stats_stub.GetPostCounters(stats_pb2.PostIdRequest(post_id=str(post_id)))
    return Counter(
        views=resp.views,
        likes=resp.likes,
        comments=resp.comments,
    )


@stats_router.get("/posts/{post_id}/timeline/{metric}", response_model=TimelineResponse)
async def post_timeline(post_id: str, metric: str = Path(pattern="views|likes|comments")):
    kind = {"views": 0, "likes": 1, "comments": 2}[metric]
    resp = await stats_stub.GetPostTimeline(
        stats_pb2.TimelineRequest(post_id=post_id, metric=kind)
    )
    return TimelineResponse(
        points=[TimelinePoint(date=p.date, value=p.value) for p in resp.points]
    )


@stats_router.get("/top/posts/{metric}", response_model=list[TopItem])
async def top_posts(metric: str = Path(pattern="views|likes|comments")):
    kind = {"views": 0, "likes": 1, "comments": 2}[metric]
    resp = await stats_stub.GetTopPosts(stats_pb2.TopPostsRequest(metric=kind))
    return [TopItem(id=p.post_id, value=p.value) for p in resp.posts]


@stats_router.get("/top/users/{metric}", response_model=list[TopItem])
async def top_users(metric: str = Path(pattern="views|likes|comments")):
    kind = {"views": 0, "likes": 1, "comments": 2}[metric]
    resp = await stats_stub.GetTopUsers(stats_pb2.TopUsersRequest(metric=kind))
    return [TopItem(id=u.user_id, value=u.value) for u in resp.users]


app.include_router(router, tags=["Posts"])
app.include_router(comments_router, tags=["Comments"])
app.include_router(actions_router, tags=["Actions"])
app.include_router(stats_router, tags=["Stats"])
