
# API Test Automation Runner

A small FastAPI-based project for testing external REST APIs.

The goal of this project is to build a lightweight API test runner that can send requests to other backend services, evaluate their responses and return structured test results.


## Tech Stack

* Python
* FastAPI
* Uvicorn
* HTTPX
* pytest

Planned:

* more API test cases
* Docker support
* Docker Compose setup
* Kubernetes deployment files
* CI/CD pipeline

## Project Idea

The API Test Automation Runner acts as a small service that can test other APIs.

Example flow:

```text
User / Browser
→ FastAPI Test Runner
→ HTTPX sends request to target API
→ Response is evaluated
→ Test result is returned as JSON
```

## Run Locally

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate.fish
```

Install dependencies:

```bash
.venv/bin/pip install -r requirements.txt
```

Start the FastAPI server:

```bash
.venv/bin/uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

## Run Tests

```bash
.venv/bin/python -m pytest
```

