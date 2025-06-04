import asyncio, json, aiokafka, uuid, pytest
import postservice_pb2 as pb
from postservice_pb2_grpc import PostServiceStub

pytestmark = pytest.mark.asyncio


async def test_view_event_produced(grpc_post_server, kafka_container):
    repo, _, ch = grpc_post_server
    stub = PostServiceStub(ch)
    producer_addr = kafka_container

    stub._channel._producer.bootstrap_servers = producer_addr

    p = await stub.CreatePost(pb.CreatePostRequest(
        title="kfk", description="", creator_id="alice"
    ))

    await stub.ViewPost(pb.ViewPostRequest(post_id=p.post.id, viewer_id="bob"))

    consumer = aiokafka.AIOKafkaConsumer(
        "post_views", bootstrap_servers=producer_addr,
        value_deserializer=lambda x: json.loads(x.decode())
    )
    await consumer.start()
    try:
        msg = await asyncio.wait_for(consumer.getone(), timeout=5)
        assert msg.value["post_id"] == p.post.id
    finally:
        await consumer.stop()


async def test_consumer_saves_to_clickhouse(clickhouse_container, kafka_container):
    producer = aiokafka.AIOKafkaProducer(bootstrap_servers=kafka_container,
                                         value_serializer=lambda x: json.dumps(x).encode())
    await producer.start()
    evt = {"post_id": str(uuid.uuid4()), "viewer_id": "alice",
           "timestamp": datetime.datetime.utcnow().isoformat()}
    await producer.send_and_wait("post_views", evt)
    await producer.stop()

    from stats_service.service import consume_loop
    task = asyncio.create_task(consume_loop())
    await asyncio.sleep(2)
    task.cancel()

    v = clickhouse_container.execute(
        "SELECT count() FROM stats.events WHERE post_id = %(pid)s", {"pid": uuid.UUID(evt["post_id"])}
    )[0][0]
    assert v == 1
