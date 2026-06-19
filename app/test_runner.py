from app.api_client import get_health


async def health_check():
    response = await get_health()
    status_code = response.status_code
    text = response.text
    passed = status_code == 200

    return {
        "test_name": "health_check",
        "target_endpoint": "http://localhost:8080/health",
        "status_code": status_code,
        "passed": passed,
        "response_body": text,
    }
