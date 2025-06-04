import pytest, grpc
import postservice_pb2 as pb
from uuid import uuid4

pytestmark = pytest.mark.asyncio


async def test_create_post_saves_to_db(grpc_post_server):
    repo, _, ch = grpc_post_server
    stub = pb.postservice_pb2_grpc.PostServiceStub(ch)

    resp = await stub.CreatePost(pb.CreatePostRequest(
        title="T", description="D", creator_id="alice", is_private=False, tags=["x"]
    ))

    db_obj = await repo.get(uuid4(resp.post.id))
    assert db_obj.title == "T"
    assert db_obj.tags == ["x"]


async def test_get_post_private_denied(grpc_post_server):
    _, _, ch = grpc_post_server
    stub = pb.postservice_pb2_grpc.PostServiceStub(ch)

    post = await stub.CreatePost(pb.CreatePostRequest(
        title="T", description="D", creator_id="bob", is_private=True
    ))

    with pytest.raises(grpc.aio.AioRpcError) as exc:
        await stub.GetPost(pb.GetPostRequest(post_id=post.post.id, requester_id="alice"))
    assert exc.value.code() == grpc.StatusCode.PERMISSION_DENIED


async def test_list_posts_filters_private(grpc_post_server):
    repo, _, ch = grpc_post_server
    stub = pb.postservice_pb2_grpc.PostServiceStub(ch)

    await stub.CreatePost(pb.CreatePostRequest(
        title="pub", description="", creator_id="bob", is_private=False
    ))
    await stub.CreatePost(pb.CreatePostRequest(
        title="priv", description="", creator_id="bob", is_private=True
    ))

    r = await stub.ListPosts(pb.ListPostsRequest(requester_id="alice", creator_id="bob", page=1, page_size=10))
    titles = [p.title for p in r.posts]
    assert titles == ["pub"]
