import asyncio, grpc, pytest
from postservice_pb2_grpc import PostServiceServicer, add_PostServiceServicer_to_server
from post_comment_service.service import PostServiceServicer as Impl
from repositories.postgres.repository import PostgresPostRepository, PostgresCommentRepository
from aiokafka import AIOKafkaProducer
from uuid import uuid4


@pytest.fixture
async def grpc_post_server(pg_container, kafka_container):
    repo = PostgresPostRepository(pg_container.get_connection_url())
    await repo.create_tables()
    comment_repo = PostgresCommentRepository(pg_container.get_connection_url())
    await comment_repo.create_tables()

    class _Dummy:
        async def send_and_wait(self, *_): pass

    producer = _Dummy()

    server = grpc.aio.server()
    add_PostServiceServicer_to_server(
        Impl(post_repo=repo, comment_repo=comment_repo, kafka_producer=producer),
        server
    )
    port = server.add_insecure_port("localhost:0")
    await server.start()
    stub_ch = grpc.aio.insecure_channel(f"localhost:{port}")
    yield repo, comment_repo, stub_ch
    await server.stop(0)
