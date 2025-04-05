import grpc
import pytest

import postservice_pb2


@pytest.mark.asyncio
async def test_create_post(grpc_client):
    create_request = postservice_pb2.CreatePostRequest(
        title="Test Title",
        description="Test Description",
        creator_id="user123",
        is_private=False,
        tags=["tag1", "tag2"],
    )
    response = await grpc_client.CreatePost(create_request)
    assert response.post.title == "Test Title"
    assert response.post.creator_id == "user123"

@pytest.mark.asyncio
async def test_get_post_access_denied(grpc_client, post_repository):
    create_request = postservice_pb2.CreatePostRequest(
        title="Private Post",
        description="Secret",
        creator_id="user123",
        is_private=True,
        tags=["private"],
    )
    create_response = await grpc_client.CreatePost(create_request)
    post_id = create_response.post.id

    get_request = postservice_pb2.GetPostRequest(
        post_id=post_id,
        requester_id="user456"
    )
    try:
        await grpc_client.GetPost(get_request)
        assert False, "Ожидалась ошибка PERMISSION_DENIED"
    except grpc.aio.AioRpcError as err:
        assert err.code() == grpc.StatusCode.PERMISSION_DENIED
