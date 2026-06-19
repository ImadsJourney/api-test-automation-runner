import httpx
from app.config import HEALTH_ENDPOINT


async def get_health():
    async with httpx.AsyncClient() as client:
        response = await client.get(HEALTH_ENDPOINT, timeout=5.0)
        return response
