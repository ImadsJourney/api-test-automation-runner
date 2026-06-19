import httpx

from app.api_client import get_health
from app.config import HEALTH_ENDPOINT


async def health_check():
    try:
        response = await get_health()
        status_code = response.status_code
        text = response.text
        passed = status_code == 200

        return {
            "test_name": "health_check",
            "target_endpoint": HEALTH_ENDPOINT,
            "status_code": status_code,
            "passed": passed,
            "response_body": text,
        }
    except httpx.RequestError as error:
        return {
            "test_name": "health_check",
            "target_endpoint": HEALTH_ENDPOINT,
            "status_code": None,
            "passed": False,
            "error": str(error),
        }
