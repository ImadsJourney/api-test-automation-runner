import asyncio

import httpx

from app import api_client


class FakeClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

    async def request(self, method, url, json, timeout):
        assert method == "POST"
        assert url == "http://localhost:8080/users"
        assert json == {"name": "Thomas"}
        assert timeout == 5.0

        return httpx.Response(201, text="Created")


def test_send_request(monkeypatch):
    monkeypatch.setattr(api_client.httpx, "AsyncClient", FakeClient)

    response = asyncio.run(
        api_client.send_request(
            "http://localhost:8080/users",
            "POST",
            {"name": "Thomas"},
        )
    )

    assert response.status_code == 201
    assert response.text == "Created"
