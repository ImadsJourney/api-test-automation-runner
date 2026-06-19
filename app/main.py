from fastapi import FastAPI
from pydantic import BaseModel
from app.runner import health_check

app = FastAPI()


class ApiTest(BaseModel):
    url: str
    method: str
    expected_status: int


@app.get("/")
async def root():
    return {"message": "API Test Runner is running."}


@app.get("/run/health")
async def run_health_check():
    return await health_check()


@app.post("/run")
async def run_test(test: ApiTest):
    return {
        "url": test.url,
        "method": test.method,
        "expected_status": test.expected_status,
    }
