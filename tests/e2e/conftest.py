import subprocess, time, pytest, httpx, os, pathlib, signal, json, jwt

COMPOSE_FILE = pathlib.Path(__file__).parent.parent.parent / "docker-compose.yml"


@pytest.fixture(scope="session", autouse=True)
def compose_up():
    proc = subprocess.Popen(["docker", "compose", "-f", str(COMPOSE_FILE), "up", "--build"],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        time.sleep(25)
        yield
    finally:
        proc.send_signal(signal.SIGINT)
        proc.wait()
