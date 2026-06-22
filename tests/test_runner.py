import asyncio
import httpx

from app import runner


class FakeResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


#### Fake Functions for health tests
async def fake_get_health():
    return FakeResponse(200, "OK")


async def fake_internal_server_error():
    return FakeResponse(500, "Internal Server Error")


async def fake_request_error():
    raise httpx.RequestError("Connection failed")


#### Fake functions for api run tests
async def fake_send_request(url: str, method: str, body: dict | None):
    assert url == "http://localhost:8080/health"
    assert method == "GET"
    return FakeResponse(200, "OK")


async def fake_internal_server_error_api_run(url: str, method: str, body: dict | None):
    assert url == "http://localhost:8080/health"
    assert method == "GET"
    return FakeResponse(500, "Internal Server Error")


async def fake_request_error_api_run(url: str, method: str, body: dict | None):
    raise httpx.RequestError("Connection failed")


def test_health_check_runs(monkeypatch):
    monkeypatch.setattr(runner, "get_health", fake_get_health)
    result = asyncio.run(runner.health_check())

    assert result["passed"] is True
    assert result["status_code"] == 200


def test_health_check_fail(monkeypatch):
    monkeypatch.setattr(runner, "get_health", fake_internal_server_error)
    result = asyncio.run(runner.health_check())

    assert result["passed"] is False
    assert result["status_code"] == 500


def test_request_error(monkeypatch):
    monkeypatch.setattr(runner, "get_health", fake_request_error)
    result = asyncio.run(runner.health_check())

    assert result["passed"] is False
    assert result["status_code"] is None
    assert result["error"] == "Connection failed"


def test_run_api(monkeypatch):
    monkeypatch.setattr(runner, "send_request", fake_send_request)
    result = asyncio.run(
        runner.run_api("http://localhost:8080/health", "GET", 200, None)
    )

    assert result["passed"] is True
    assert result["status_code"] == 200
    assert result["expected_status"] == 200
    assert result["target_endpoint"] == "http://localhost:8080/health"
    assert result["response_body"] == "OK"


def test_run_api_fail(monkeypatch):
    monkeypatch.setattr(runner, "send_request", fake_internal_server_error_api_run)
    result = asyncio.run(
        runner.run_api("http://localhost:8080/health", "GET", 200, None)
    )

    assert result["status_code"] == 500
    assert result["passed"] is False


def test_run_api_request_error(monkeypatch):
    monkeypatch.setattr(runner, "send_request", fake_request_error_api_run)
    result = asyncio.run(
        runner.run_api("http://localhost:8080/health", "GET", 200, None)
    )

    assert result["status_code"] is None
    assert result["passed"] is False
    assert result["error"] == "Connection failed"
