import httpx

BASE_URL = "http://localhost:8080"


async def get_health():
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL + "/health")
        return response
