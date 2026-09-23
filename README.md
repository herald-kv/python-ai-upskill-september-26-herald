# Secret Journal

A journaling app that started as a Python CLI (Day 1) and is now also a FastAPI
web API with a small browser frontend (Day 2). The CLI and the API share the
same storage, `data/journal.csv`.

## Project structure

```
├── src/
│   ├── cli/journal_cli.py          # Day 1 terminal app
│   ├── api/
│   │   ├── main.py                 # FastAPI app, CORS, error handlers, "/" route
│   │   ├── routers/journal_routes.py   # GET/POST /journal
│   │   ├── models/journal_model.py     # Pydantic request/response models
│   │   └── utils/file_handler.py   # CSV read/write (shared with the CLI)
│   └── core/config.py              # Paths, limits, CORS origins
├── data/journal.csv                # Created on first save (git-ignored)
├── frontend.html                   # Minimal browser UI
├── requirements.txt
└── README.md
```

## ⚙️ Setup

Requires Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Running

**API server** (from the project root):

```bash
uvicorn src.api.main:app --reload
```

- API: http://localhost:8000
- Interactive docs (Swagger UI): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Frontend:** with the server running, open `frontend.html` in a browser.

**CLI:**

```bash
python -m src.cli.journal_cli
```

**Formatting / linting:**

```bash
black src/
isort src/
flake8
```

## 📌 API endpoints

### `GET /`

Health check.

```json
{ "message": "Journal API is running 🚀" }
```

### `GET /journal`

Returns all entries, oldest first.

| Query param        | Required | Values                              |
| ------------------ | -------- | ----------------------------------- |
| `sentiment_filter` | No       | `positive`, `negative`, `neutral`   |

Sentiment comes from the entry's mood: `happy` = positive, `sad` = negative,
`neutral` = neutral.

```bash
curl "http://localhost:8000/journal?sentiment_filter=positive"
```

**200 OK**

```json
[
  {
    "id": 1,
    "entry": "Today I learned FastAPI. It feels great!",
    "mood": "happy",
    "mood_symbol": ":)",
    "sentiment": "positive",
    "timestamp": "2026-09-23 22:48"
  }
]
```

An invalid filter value returns **422**:

```json
{ "message": "Input should be 'positive', 'negative' or 'neutral'", "detail": [...] }
```

### `POST /journal`

Creates an entry. The mood is stored in the CSV as the Day 1 ASCII face
(`happy` → `:)`, `sad` → `:(`, `neutral` → `:|`).

**Request body**

```json
{ "entry": "Today I learned FastAPI. It feels great!", "mood": "happy" }
```

Validation:
- `entry` is required, is trimmed of surrounding whitespace, must not be
  empty, and can be at most 500 characters.
- `mood` is required and must be `happy`, `sad` or `neutral` (any case).

```bash
curl -X POST http://localhost:8000/journal \
  -H "Content-Type: application/json" \
  -d '{"entry": "Today I learned FastAPI. It feels great!", "mood": "happy"}'
```

**201 Created**

```json
{
  "message": "Journal entry saved successfully.",
  "data": {
    "id": 1,
    "entry": "Today I learned FastAPI. It feels great!",
    "mood": "happy",
    "mood_symbol": ":)",
    "sentiment": "positive",
    "timestamp": "2026-09-23 22:48"
  }
}
```

**422 Unprocessable Content**

```json
{ "message": "Journal entry cannot be empty.", "detail": [...] }
```

```json
{ "message": "Journal entry cannot exceed 500 characters (got 501).", "detail": [...] }
```

```json
{ "message": "Input should be 'happy', 'sad' or 'neutral'", "detail": [...] }
```

Every error response has a top-level `message`, so clients can always show
`result.message`.

## 🧠 Day 2 learnings

- **Client/server basics:** a browser (client) sends HTTP requests to a server;
  the method (`GET` to read, `POST` to create) and the status code (`200`,
  `201`, `422`, `500`) describe what happened.
- **FastAPI routing:** `APIRouter` groups related endpoints and is plugged into
  the app with `include_router`, which keeps `main.py` small.
- **Query parameters vs. request bodies:** optional filters go in the URL
  (`?sentiment_filter=...`), and data being created goes in a JSON body.
- **Pydantic validation:** type hints and validators reject bad input before
  the route runs, and an `Enum` limits a field (like `mood`) or a query
  parameter to a fixed set of values.
- **CORS:** browsers block a page from calling an API on a different origin
  unless the server sends `Access-Control-Allow-*` headers. `CORSMiddleware`
  adds them. It's set to `*` for local development only.
- **Reusing logic:** moving CSV handling into `file_handler.py` lets the CLI
  and the API share one implementation, so both write the same file format.
- **Free docs:** FastAPI builds OpenAPI docs at `/docs` from the route
  docstrings, type hints and model examples.
