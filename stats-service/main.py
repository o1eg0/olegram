import asyncio, json, os, signal, logging
from datetime import datetime, timezone
from uuid import UUID

import grpc
from aiokafka import AIOKafkaConsumer
from clickhouse_driver import Client
import stats_pb2, stats_pb2_grpc

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("stats-service")

def apply_ch_migration(client):
    with open("001_init.sql", "r") as f:
        CH_MIGRATION = f.read()
    for statement in CH_MIGRATION.strip().split(';'):
        stmt = statement.strip()
        if stmt:
            try:
                client.execute(stmt)
            except Exception as ex:
                print(f"Migration failed: {ex} | SQL: {stmt[:60]}")

CH_FOR_MIGRATION = Client(
    host=os.getenv("CH_HOST", "clickhouse"),
    port=int(os.getenv("CH_PORT", 9000)),
    database="default",      # <--- IMPORTANT!
    send_receive_timeout=10,
)
apply_ch_migration(CH_FOR_MIGRATION)

CH = Client(
    host=os.getenv("CH_HOST", "clickhouse"),
    port=int(os.getenv("CH_PORT", 9000)),
    database="stats",
    send_receive_timeout=10,
)


async def consume_loop():
    consumer = AIOKafkaConsumer(
        "post_views", "post_likes", "post_comments",
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP", "kafka:9092"),
        value_deserializer=lambda x: json.loads(x.decode()),
        enable_auto_commit=True,
    )
    await consumer.start()
    try:
        async for msg in consumer:
            evt_type = (
                1 if msg.topic == "post_views" else
                2 if msg.topic == "post_likes" else
                3
            )
            data = msg.value
            CH.execute(
                "INSERT INTO stats.events "
                "(event_time, event_type, post_id, user_id) "
                "VALUES",
                [
                    (
                        datetime.fromisoformat(data["timestamp"]).replace(tzinfo=timezone.utc),
                        evt_type,
                        UUID(data["post_id"]),
                        data.get("viewer_id") or data.get("user_id"),
                    )
                ],
            )
    finally:
        await consumer.stop()


# --- gRPC сервис -----------------------------------------------

def _metric_column(kind: int) -> str:
    return {0: "views", 1: "likes", 2: "comments"}[kind]


class StatsService(stats_pb2_grpc.StatsServiceServicer):
    def GetPostCounters(self, request, context):
        result = CH.execute(
            f"""
            SELECT sum(views), sum(likes), sum(comments)
            FROM stats.post_daily_agg
            WHERE post_id = %(pid)s
            """,
            {"pid": UUID(request.post_id)},
        )[0]
        return stats_pb2.PostCountersResponse(
            views=result[0] or 0,
            likes=result[1] or 0,
            comments=result[2] or 0,
        )

    def GetPostTimeline(self, request, context):
        col = _metric_column(request.metric)
        rows = CH.execute(
            f"""
            SELECT event_date, sum({col}) AS v
            FROM stats.post_daily_agg
            WHERE post_id = %(pid)s
            GROUP BY event_date
            ORDER BY event_date
            """,
            {"pid": UUID(request.post_id)},
        )
        return stats_pb2.TimelineResponse(
            points=[
                stats_pb2.TimelinePoint(date=str(r[0]), value=r[1]) for r in rows
            ]
        )

    def GetTopPosts(self, request, context):
        col = _metric_column(request.metric)
        rows = CH.execute(
            f"""
            SELECT post_id, sum({col}) AS v
            FROM stats.post_daily_agg
            GROUP BY post_id
            ORDER BY v DESC
            LIMIT 10
            """
        )
        return stats_pb2.TopPostsResponse(
            posts=[stats_pb2.TopPost(post_id=str(r[0]), value=r[1]) for r in rows]
        )

    def GetTopUsers(self, request, context):
        col = _metric_column(request.metric)
        rows = CH.execute(
            f"""
            SELECT user_id, sum({col}) AS v
            FROM stats.user_daily_agg
            GROUP BY user_id
            ORDER BY v DESC
            LIMIT 10
            """
        )
        return stats_pb2.TopUsersResponse(
            users=[stats_pb2.TopUser(user_id=r[0], value=r[1]) for r in rows]
        )


async def serve():
    server = grpc.aio.server()
    stats_pb2_grpc.add_StatsServiceServicer_to_server(StatsService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(consume_loop())
    loop.run_until_complete(serve())
