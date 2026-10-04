# Cloud Resource Status API

A FastAPI capstone project that displays cloud service health, sample EC2 instances, and AI-generated operational guidance in a web dashboard.

The cloud checks are simulated: the application does not connect to AWS. Instance data is stored in memory, while AI analysis makes real requests to the OpenAI API.

## Features

- Concurrent EC2, RDS, and EKS health checks using `asyncio.gather`.
- Per-service timeout handling and failure reporting.
- API endpoints for platform health and instance lookup.
- Dashboard with service indicators, an instance table, and a Refresh button.
- Structured AI analysis with severity, summary, possible impact, and recommended checks.
- Tests for API responses, instance lookup, and check success, failure, and timeout behavior.

## Technology

Python, FastAPI, Uvicorn, asyncio, Pydantic, Jinja2, the OpenAI Python SDK, vanilla JavaScript, CSS, and pytest.

## Local setup

Use **Python 3.11 or newer**. Although `pyproject.toml` currently declares Python 3.10+, the checks use `asyncio.timeout`, which requires Python 3.11+.

Run the following commands from the project directory containing `app/` and `pyproject.toml`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn jinja2 pydantic openai
python -m pip install pytest pytest-asyncio httpx
```

Dependencies are not yet listed in `pyproject.toml`, so install them explicitly as shown above.

### Configuration

Set these environment variables in the terminal where you will start the server:

```bash
export OPENAI_API_KEY="your_api_key_here"
export OPENAI_MODEL="gpt-6-astra"
```

| Variable | Required | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | Yes | Credentials for the OpenAI client, which is initialized when the app imports. |
| `OPENAI_MODEL` | No | Model used for analysis; defaults to `gpt-6-astra` in `app/ai_analysis.py`. |

Choose a model available to your API project that supports the structured response used by the application. Keep API keys out of source control. The application does not currently load `.env` files automatically.

### Start the server

```bash
python -m uvicorn app.main:app --reload
```

Run this from the project directory because template and static file paths are relative to it.

- Dashboard: <http://127.0.0.1:8000/dashboard>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- Health endpoint: <http://127.0.0.1:8000/health>

The dashboard loads status on page load and when **Refresh** is clicked. Each dashboard analysis request calls the OpenAI API and may incur API usage charges.

## API endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Application health; returns `{"status":"healthy"}`. |
| GET | `/instances` | List the sample instances. |
| GET | `/instances/{instance_id}` | Retrieve an instance; returns 404 if it is unknown. |
| GET | `/platform-status` | Run the simulated EC2, RDS, and EKS checks concurrently. |
| POST | `/ai/analyze` | Analyze the service status supplied in the JSON request body. |
| GET | `/dashboard` | Render the web dashboard. |

### Check platform status

```bash
curl http://127.0.0.1:8000/platform-status
```

The current simulated checks all succeed:

```json
{
  "ec2": "healthy",
  "rds": "healthy",
  "eks": "healthy"
}
```

The check wrapper returns `failed` when a check raises an exception and `timeout` when it exceeds the default three-second limit.

### Request AI analysis

```bash
curl -X POST http://127.0.0.1:8000/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"ec2":"healthy","rds":"failed","eks":"healthy"}'
```

This endpoint analyzes the supplied snapshot; it does not run fresh cloud checks. Its response contains:

| Field | Content |
| --- | --- |
| `severity` | `healthy`, `degraded`, or `critical` |
| `summary` | A concise assessment of the supplied status |
| `possible_impact` | Potential operational impact |
| `recommended_checks` | A list of suggested follow-up checks |

The application calculates severity before requesting analysis:

| Services with a status other than `healthy` | Severity |
| --- | --- |
| 0 | `healthy` |
| 1 | `degraded` |
| 2 or more | `critical` |

The model is instructed to preserve that severity and avoid inventing metrics, incidents, or root causes. The returned severity is currently validated against the allowed labels, but is not checked for equality with the calculated value.

## Tests

```bash
OPENAI_API_KEY=test-placeholder python -m pytest -q
```

The placeholder allows the OpenAI client to initialize during test collection. The existing tests do not call the OpenAI API or test the AI analysis endpoint.

## Project structure

```text
app/
├── main.py                  # FastAPI routes and dashboard setup
├── checks.py                # Simulated checks, timeouts, and severity calculation
├── services.py              # In-memory instance data and lookup
├── models.py                # Request and response schemas
├── ai_analysis.py           # OpenAI structured analysis
├── templates/
│   └── dashboard.html       # Dashboard markup
└── static/
    ├── dashboard.js         # Data fetching and dashboard updates
    └── styles.css           # Dashboard styles
tests/
├── test_api.py
├── test_checks.py
└── test_services.py
pyproject.toml
```

## Current limitations and troubleshooting

- **Missing credentials at startup:** export `OPENAI_API_KEY` in the same terminal before starting Uvicorn. A key is required at import time even for non-AI routes.
- **AI error handling:** `main.py` currently references an undefined `logger` in the analysis exception handler. Define `logger = logging.getLogger(__name__)` after importing `logging` to allow the intended HTTP 502 response to be raised when analysis fails.
- **Dashboard severity:** the overall dashboard badge shows `DEGRADED` for any unhealthy service count; the AI severity calculation also distinguishes `critical`.
- **Duplicate dashboard requests:** the template contains an inline dashboard loader as well as loading `dashboard.js`, so initial page load can fetch status and instances more than once.
- **Demo scope:** cloud status and instance data are simulated, with no persistence or authentication implemented.
