import stats_pb2 as pb, pytest, datetime, uuid

pytestmark = pytest.mark.asyncio


async def _insert_dummy(ch, post_id, user_id):
    today = datetime.date.today()
    ch.execute(
        "INSERT INTO stats.post_daily_agg (event_date, post_id, views, likes, comments) VALUES",
        [(today, uuid.UUID(post_id), 5, 2, 1)]
    )
    ch.execute(
        "INSERT INTO stats.user_daily_agg (event_date, user_id, views, likes, comments) VALUES",
        [(today, user_id, 5, 2, 1)]
    )


async def test_get_post_counters(grpc_stats_server):
    ch, stub = grpc_stats_server
    pid = str(uuid.uuid4())
    await _insert_dummy(ch, pid, "alice")

    r = await stub.GetPostCounters(pb.PostIdRequest(post_id=pid))
    assert (r.views, r.likes, r.comments) == (5, 2, 1)


async def test_post_timeline_grouping(grpc_stats_server):
    ch, stub = grpc_stats_server
    pid = str(uuid.uuid4())
    await _insert_dummy(ch, pid, "bob")

    r = await stub.GetPostTimeline(pb.TimelineRequest(post_id=pid, metric=0))
    assert len(r.points) == 1
    assert r.points[0].value == 5


async def test_top_users_sorted(grpc_stats_server):
    ch, stub = grpc_stats_server
    await _insert_dummy(ch, str(uuid.uuid4()), "topper")
    await _insert_dummy(ch, str(uuid.uuid4()), "mid")

    r = await stub.GetTopUsers(pb.TopUsersRequest(metric=0))
    assert r.users[0].user_id == "topper"
