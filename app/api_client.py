import httpx
from app.config import HEALTH_ENDPOINT


async def get_health():
    async with httpx.AsyncClient() as client:
        response = await client.get(HEALTH_ENDPOINT, timeout=5.0)
        return response


async def send_request(url: str, method: str, body: dict | None):
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, json=body, timeout=5.0)
        return response
