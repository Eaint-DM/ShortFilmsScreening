
"""Application composition root and HTTP error translation."""

import logging
import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.application.service import (
    StarterService,
    ValidationError,
    NotFoundError,
    ConflictError,
)
from app.infrastructure.postgres import PostgresData
from app.presentation.api import routes


def build_service(database_url: str) -> StarterService:
    database = PostgresData(database_url)
    return StarterService(database, database)


def create_app(service: StarterService | None = None):
    app = FastAPI(
        title="S02 Short-Film Screening Programme API",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    app.include_router(
        routes(service or build_service(os.environ["DATABASE_URL"]))
    )

    @app.exception_handler(ValidationError)
    async def invalid_business_rule(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=400,
            content={"error_code": "INVALID_REQUEST", "message": str(exc)},
        )

    @app.exception_handler(NotFoundError)
    async def not_found(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content={"error_code": "NOT_FOUND", "message": str(exc)},
        )

    @app.exception_handler(ConflictError)
    async def conflict(request: Request, exc: ConflictError):
        return JSONResponse(
            status_code=409,
            content={"error_code": "CONFLICT", "message": str(exc)},
        )

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=400,
            content={
                "error_code": "INVALID_REQUEST",
                "message": "Check request fields and X-Session-Code.",
            },
        )

    @app.exception_handler(Exception)
    async def unavailable(request: Request, exc: Exception):
        logging.exception("Request failed: %s", request.url.path)
        return JSONResponse(
            status_code=503,
            content={
                "error_code": "SERVICE_UNAVAILABLE",
                "message": "Check API/database logs.",
            },
        )

    return app


app = create_app()
