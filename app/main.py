from enum import Enum

from fastapi import FastAPI
from pydantic import AnyHttpUrl, BaseModel, Field
from app.runner import health_check, run_api

app = FastAPI()


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class ApiTest(BaseModel):
    url: AnyHttpUrl
    method: HttpMethod
    expected_status: int = Field(ge=100, le=599)
    body: dict | None = None


@app.get("/")
async def root():
    return {"message": "API Test Runner is running."}


@app.get("/run/health")
async def run_health_check():
    return await health_check()


@app.post("/run")
async def run_test(test: ApiTest):
    return await run_api(
        str(test.url), test.method.value, test.expected_status, test.body
    )
