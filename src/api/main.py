"""FastAPI application entry point.

Run from the project root with:
    uvicorn src.api.main:app --reload
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from src.api.routers import journal_routes
from src.core.config import API_DESCRIPTION, API_TITLE, API_VERSION, CORS_ORIGINS

app = FastAPI(title=API_TITLE, description=API_DESCRIPTION, version=API_VERSION)

# Browsers block requests from one origin (e.g. a frontend on another port or
# a file opened from disk) to another unless the server explicitly allows it.
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(journal_routes.router)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request, error: RequestValidationError
) -> JSONResponse:
    """Return validation errors with a readable top-level "message"."""
    first_error = error.errors()[0]
    # Pydantic prefixes custom validator messages with "Value error, ".
    message = first_error["msg"].removeprefix("Value error, ")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"message": message, "detail": jsonable_errors(error)},
    )


@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, error: HTTPException) -> JSONResponse:
    """Return HTTP errors (including 404s) in the same {"message": ...} shape."""
    return JSONResponse(
        status_code=error.status_code,
        content={"message": error.detail},
        headers=error.headers,
    )


def jsonable_errors(error: RequestValidationError) -> list[dict]:
    """Keep only the JSON-safe parts of each validation error."""
    return [
        {"loc": item["loc"], "msg": item["msg"], "type": item["type"]}
        for item in error.errors()
    ]


@app.get("/", tags=["Health"])
def read_root() -> dict:
    """Landing route confirming the API is up."""
    return {"message": "Journal API is running 🚀"}
