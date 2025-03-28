import os

import httpx
from fastapi import FastAPI, Request

app = FastAPI(title="API Gateway")
USER_SERVICE_URL = os.getenv("USER_SERVICE_ADDR")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"http://{USER_SERVICE_URL}/{path}"
        response = await client.request(
            method=request.method,
            url=url,
            params=request.query_params,
            content=await request.body(),
            headers=request.headers.raw
        )
    return response.json()
