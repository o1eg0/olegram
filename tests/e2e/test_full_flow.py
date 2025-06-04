import pytest, time, uuid, httpx

BASE = "http://localhost:8081"


@pytest.mark.asyncio
async def test_register_create_like_stats():
    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE}/users/register", json=dict(username="alice", password="123"))
        await client.post(f"{BASE}/users/register", json=dict(username="bob", password="123"))

        resp = await client.post(f"{BASE}/users/login", data=dict(username="alice", password="123"))
        token_a = resp.cookies["jwt-token"]

        resp = await client.post(f"{BASE}/posts", json={
            "title": "promo", "description": "spring", "is_private": False, "tags": []
        }, headers={"jwt-token": token_a})
        post_id = resp.json()["id"]

        resp = await client.post(f"{BASE}/users/login", data=dict(username="bob", password="123"))
        token_b = resp.cookies["jwt-token"]
        await client.post(f"{BASE}/posts/{post_id}/like", headers={"jwt-token": token_b})

        time.sleep(5)

        r = await client.get(f"{BASE}/stats/posts/{post_id}", headers={"jwt-token": token_a})
        assert r.json()["likes"] == 1
