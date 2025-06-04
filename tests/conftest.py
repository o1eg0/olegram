import asyncio, os
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.kafka import KafkaContainer
from clickhouse_driver import Client as CHClient


@pytest.fixture(scope="session")
def pg_container():
    with PostgresContainer("postgres:16") as pg:
        yield pg


@pytest.fixture(scope="session")
def clickhouse_container():
    import docker, time, random, string
    client = docker.from_env()
    tag = "clickhouse/clickhouse-server:23.10"
    cont = client.containers.run(
        tag, detach=True, ports={'9000/tcp': None},
        ulimits=[docker.types.Ulimit(name='nofile', soft=262144, hard=262144)]
    )
    time.sleep(8)
    host_port = cont.attrs['NetworkSettings']['Ports']['9000/tcp'][0]['HostPort']
    ch = CHClient(host="localhost", port=int(host_port))
    yield ch
    cont.stop();
    cont.remove()


@pytest.fixture(scope="session")
def kafka_container():
    with KafkaContainer() as kafka:
        yield kafka.get_bootstrap_server()
