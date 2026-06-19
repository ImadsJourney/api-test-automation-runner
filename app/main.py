from fastapi import FastAPI
from app.runner import health_check

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "API Test Runner is running."}


@app.get("/run/health")
async def run_health_check():
    return await health_check()
