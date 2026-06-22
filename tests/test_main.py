from fastapi.testclient import TestClient

from app.main import app

from app import main

client = TestClient(app)

# TestClient ist eine weitere Funktion von FastAPI
# welches uns erlaubt einen client zu simulieren
# ohne unseren tatsächlichen Server anzuschalten
# und ein echten Client zu benötigen
#
# client = TestClient(app) erstellt den Fake-Client
# der an unsere app gebunden ist
#
# die function simuliert den tatächlichen HTTP-Aufruf
# an meine app und speichert die HTTP-Antwort in response
# dann schauen wir in der response also die antwort unserer app
# status code = 200 ist und der json body ein key "message" hat mit "API Test Runner is running." als Wert


def test_root_route():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API Test Runner is running."}


async def fake_health_check():
    return {
        "test_name": "health_check",
        "status_code": 200,
        "passed": True,
        "response_body": "OK",
    }


def test_run_health_check(monkeypatch):
    monkeypatch.setattr(main, "health_check", fake_health_check)

    response = client.get("/run/health")

    assert response.status_code == 200
    assert response.json()["passed"] is True
    assert response.json()["response_body"] == "OK"


async def fake_run_api(url: str, method: str, expected_status: int, body: dict | None):
    assert method == "POST"
    assert url == "http://localhost:8080/health"
    assert expected_status == 200
    assert body == {"name": "Thomas"}

    return {
        "test_name": "run_api_test",
        "target_endpoint": url,
        "expected_status": expected_status,
        "status_code": 200,
        "response_body": "OK",
        "passed": True,
    }


def test_run_test(monkeypatch):
    monkeypatch.setattr(main, "run_api", fake_run_api)

    response = client.post(
        "/run",
        json={
            "url": "http://localhost:8080/health",
            "method": "POST",
            "expected_status": 200,
            "body": {"name": "Thomas"},
        },
    )

    assert response.json()["passed"] is True
    assert response.status_code == 200
    assert response.json()["response_body"] == "OK"
    assert response.json()["expected_status"] == 200


def test_run_test_invalid_json():
    response = client.post(
        "/run", json={"url": "http://localhost:8080/health", "method": "GET"}
    )

    assert response.status_code == 422


def test_run_test_invalid_method():
    response = client.post(
        "/run",
        json={
            "url": "http://localhost:8080/health",
            "method": "ABC",
            "expected_status": 200,
        },
    )

    assert response.status_code == 422


def test_run_test_invalid_expected_status():
    response = client.post(
        "/run",
        json={
            "url": "http://localhost:8080/health",
            "method": "GET",
            "expected_status": 99,
        },
    )
    assert response.status_code == 422


def test_run_test_invalid_expected_status_upper_border():
    response = client.post(
        "/run",
        json={
            "url": "http://localhost:8080/health",
            "method": "GET",
            "expected_status": 600,
        },
    )
    assert response.status_code == 422


def test_run_test_invalid_http_syntax():
    response = client.post(
        "/run",
        json={
            "url": "keine-url",
            "method": "GET",
            "expected_status": 200,
        },
    )
    assert response.status_code == 422
