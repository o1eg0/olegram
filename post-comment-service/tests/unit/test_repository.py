from uuid import uuid4

import pytest

from repositories.schemas import PostCreate, PostUpdate


@pytest.mark.asyncio
async def test_create_and_get_post(post_repository):
    post_data = PostCreate(
        title="Test Post",
        description="This is a test post",
        creator_id="creator1",
        is_private=False,
        tags=["test", "post"]
    )
    created_post = await post_repository.create(post_data)
    assert created_post is not None
    assert created_post.title == post_data.title
    assert created_post.description == post_data.description
    assert created_post.creator_id == post_data.creator_id
    assert created_post.tags == post_data.tags
    assert created_post.id is not None

    post_from_db = await post_repository.get(created_post.id)
    assert post_from_db is not None
    assert post_from_db.title == created_post.title


@pytest.mark.asyncio
async def test_update_post(post_repository):
    post_data = PostCreate(
        title="Original Title",
        description="Original Description",
        creator_id="creator1",
        is_private=False,
        tags=["original"]
    )
    created_post = await post_repository.create(post_data)

    update_data = PostUpdate(
        title="Updated Title",
        description="Updated Description",
        is_private=True,
        tags=["updated"]
    )
    updated_post = await post_repository.update(created_post.id, update_data)
    assert updated_post is not None
    assert updated_post.title == "Updated Title"
    assert updated_post.description == "Updated Description"
    assert updated_post.is_private is True
    assert updated_post.tags == ["updated"]

    non_existent_post_id = uuid4()
    update_none = await post_repository.update(non_existent_post_id, update_data)
    assert update_none is None


@pytest.mark.asyncio
async def test_delete_post(post_repository):
    post_data = PostCreate(
        title="Title to be deleted",
        description="Description to be deleted",
        creator_id="creator1",
        is_private=False,
        tags=[]
    )
    created_post = await post_repository.create(post_data)

    deleted = await post_repository.delete(created_post.id)
    assert deleted is True

    post_from_db = await post_repository.get(created_post.id)
    assert post_from_db is None

    non_existent_post_id = uuid4()
    deleted_none = await post_repository.delete(non_existent_post_id)
    assert deleted_none is False


@pytest.mark.asyncio
async def test_list_posts(post_repository):
    creator_id = "creator_list"
    posts_data = [
        PostCreate(
            title=f"Post {i}",
            description=f"Description {i}",
            creator_id=creator_id,
            is_private=False,
            tags=[f"tag{i}"]
        )
        for i in range(5)
    ]
    for post_data in posts_data:
        await post_repository.create(post_data)

    posts_list, total = await post_repository.list_posts(creator_id, offset=0, limit=3)
    assert total == 5
    assert len(posts_list) == 3

    posts_list_offset, _ = await post_repository.list_posts(creator_id, offset=3, limit=3)
    assert len(posts_list_offset) == 2

    latest_post = posts_list[0]
    for post in posts_list[1:]:
        assert latest_post.created_at >= post.created_at