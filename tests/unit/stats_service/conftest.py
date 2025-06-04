import grpc, pytest, asyncio
from stats

-service.service
import StatsService, serve
from stats_pb2_grpc import add_StatsServiceServicer_to_server, StatsServiceStub


@pytest.fixture
async def grpc_stats_server(clickhouse_container):
    server = grpc.aio.server()
    add_StatsServiceServicer_to_server(StatsService(), server)
    port = server.add_insecure_port("localhost:0")
    await server.start()
    ch = grpc.aio.insecure_channel(f"localhost:{port}")
    yield clickhouse_container, StatsServiceStub(ch)
    await server.stop(0)
