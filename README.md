# Leave Management API

This repository contains a FastAPI leave management API and its test scripts.

## Requirements

- Python 3.10 or newer
- `pip`
- For the AI chat endpoint and AI test scripts: access to the Groq service

## Set up the environment

From the repository root, create and activate a virtual environment, then install the API and test dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# On Windows PowerShell, use: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r mock_api/requirements.txt
```

## Run the API

Start the development server from the `mock_api` directory:

```bash
cd mock_api
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation is at `http://127.0.0.1:8000/docs`; the root endpoint (`/`) reports that the API is running.

The SQLite database URL is `sqlite:///./leave.db`. The app creates its tables when it starts. Running Uvicorn from `mock_api` uses `mock_api/leave.db`.

The API uses demo bearer tokens defined in `mock_api/auth.py`:

| Role       | Token  |
| ---------- | ------ |
| Employee 1 | `emp1` |
| Employee 2 | `emp2` |
| Employee 3 | `emp3` |
| Employee 4 | `emp4` |
| Manager    | `man`  |

For example, create a leave request with:

```bash
curl -X POST http://127.0.0.1:8000/leave \
  -H 'Authorization: Bearer emp1' \
  -H 'Content-Type: application/json' \
  -d '{"start_date":"2029-11-01","end_date":"2029-11-02","reason":"Personal work","leave_type":"casual"}'
```

The response includes the new request's `id`. A manager approves that request by sending a `PUT` to `/leave/{id}/approve` with the manager token. Replace `1` below with the `id` returned when the request was created:

```bash
curl -X PUT http://127.0.0.1:8000/leave/1/approve \
  -H 'Authorization: Bearer man'
```

The response shows the request with `status` set to `approved` and `approved_by` set to `MGR001`. Only a pending request can be approved, and this endpoint requires the manager token.

## Run the traditional API tests

Keep the API server running in one terminal. In a second terminal, activate the same virtual environment from the repository root and run the test modules with pytest:

```bash
python -m pytest test/traditional_testing/func.py
python -m pytest test/traditional_testing/auth.py
python -m pytest test/traditional_testing/edge.py
python -m pytest test/traditional_testing/negative.py
```

To run all four modules in one command:

```bash
python -m pytest test/traditional_testing/func.py test/traditional_testing/auth.py test/traditional_testing/edge.py test/traditional_testing/negative.py
```

These tests make HTTP requests to `http://127.0.0.1:8000`, as configured in `test/traditional_testing/req.py`. They use the demo tokens above and write leave requests to the API's SQLite database.

## AI chat and AI test scripts

The AI chat endpoint is `POST /ai/chat` and requires an employee bearer token. It calls Groq. The AI scripts are `test/ai_testing/collect.py` (collect responses) and `test/ai_testing/evaluate.py` (evaluate collected responses).

The AI test scripts currently use absolute paths such as `/test/testcases/ai_test.csv`, `/test/actual_responses.json`, and `/test/result.json`. Those paths do not point to this repository's `test/` directory in a normal checkout, so the scripts need their paths configured for your environment before they can be run. The scripts also contain Groq API keys in their source; no environment-variable configuration is currently implemented.

## API routes

- `GET /` — API status
- `POST /leave` — Create a leave request (employee token required)
- `GET /leave/{leave_id}` — Retrieve a leave request (bearer token required)
- `PUT /leave/{leave_id}/approve` — Approve a pending request (manager token required)
- `POST /ai/chat` — Chat with the AI leave assistant (bearer token and Groq access required)
