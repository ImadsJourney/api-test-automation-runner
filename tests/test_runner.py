import asyncio
import httpx

from app import runner


class FakeResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


async def fake_get_health():
    return FakeResponse(200, "OK")


async def fake_internal_server_error():
    return FakeResponse(500, "Internal Server Error")


async def fake_request_error():
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
