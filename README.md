# asep-test-playground

Settings page feature for the ASEP application — lets a user view and update their preferences (theme, language, timezone, notification settings) through a frontend Settings page backed by a `/settings` REST API. This repo currently contains the frontend client/UI, containerization, CI, and tests for that feature. **No backend implementation of `/settings` exists in this run** — `settingsClient.ts` calls the endpoints described below, but the server side must be provided separately (the FastAPI/SQLAlchemy packages in `requirements.txt` are dependencies staged for that future backend work, not yet wired into any app code in this run).

## Setup

### Frontend
```bash
cd frontend
npm ci
npm test        # run unit tests (settingsClient.test.ts)
```

Set the API base URL the client talks to (defaults to `/api` if unset):
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Python (tests / tooling only)
```bash
pip install -r requirements.txt
pytest tests/e2e/          # end-to-end Settings page tests (Playwright)
```
E2e tests are skipped automatically if Playwright browser binaries aren't installed (`tests/e2e/conftest.py`). To install browsers explicitly and run them:
```bash
playwright install chromium
pytest tests/e2e/test_e2e_settings_page.py
```

### Docker
```bash
docker build -t asep-app .
docker run -p 8000:8000 asep-app
```
> Note: the Dockerfile's `CMD` (`python -m app`) is a placeholder — no Python application entry point exists in this run's codebase yet. Update `CMD` once a backend server module is added.

### CI
`.github/workflows/ci.yml` runs on push/PR to `main`: installs Python + Node dependencies, runs frontend tests (`npm test`) and Python tests (`pytest --cov`), then builds the Docker image (build-only, no push) after tests pass.

## API Endpoints

The frontend (`frontend/src/lib/settingsClient.ts`) expects a backend exposing these endpoints. (Not implemented server-side in this run.)

### GET /settings
Fetch the current user's settings.

**Response** `SettingsResponse`
```json
{
  "theme": "system",
  "language": "en",
  "timezone": "UTC",
  "email_notifications": true,
  "push_notifications": true
}
```

```bash
curl -X GET http://localhost:8000/settings
```

### PATCH /settings
Update one or more settings fields.

**Request body** `SettingsUpdate` (all fields optional)
```json
{
  "theme": "dark",
  "language": "en",
  "timezone": "America/New_York",
  "email_notifications": false,
  "push_notifications": true
}
```

**Response** `SettingsResponse` (full updated object)

```bash
curl -X PATCH http://localhost:8000/settings \
  -H "Content-Type: application/json" \
  -d '{"theme": "dark", "push_notifications": false}'
```

### POST /settings/reset
Reset settings to defaults.

**Response** `SettingsResponse` (reset to defaults)

```bash
curl -X POST http://localhost:8000/settings/reset
```

## Models

### SettingsResponse
| Field | Type | Description |
|---|---|---|
| `theme` | string | e.g. `"light"`, `"dark"`, `"system"` |
| `language` | string | e.g. `"en"` |
| `timezone` | string | e.g. `"UTC"` |
| `email_notifications` | boolean | Email notification opt-in |
| `push_notifications` | boolean | Push notification opt-in |

### SettingsUpdate
Same fields as `SettingsResponse`, all optional (partial update payload for `PATCH /settings`).

**Client-side behavior:** `fetchSettings()` caches the last successful response in `localStorage` (`app.settings.cache`) and falls back to that cache — or hardcoded defaults (`theme: "system"`, `language: "en"`, `timezone: "UTC"`, both notifications `true`) — if the network request fails, so the Settings page can render offline/on error.
