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

