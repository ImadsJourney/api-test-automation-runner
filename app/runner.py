import httpx

from app.api_client import get_health, send_request
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


async def run_api(
    url: str, method: str, expected_status: int, body: dict | None = None
):
    try:
        response = await send_request(url, method, body)
        status_code = response.status_code
        text = response.text
        passed = expected_status == status_code

        return {
            "test_name": "run_api_test",
            "target_endpoint": url,
            "expected_status": expected_status,
            "status_code": status_code,
            "response_body": text,
            "passed": passed,
        }
    except httpx.RequestError as error:
        return {
            "test_name": "run_api_test",
            "target_endpoint": url,
            "status_code": None,
            "passed": False,
            "error": str(error),
        }
