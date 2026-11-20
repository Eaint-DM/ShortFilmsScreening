
"""HTTP routes for the S02 short-film screening programme."""

from typing import Annotated

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field, StrictInt

from app.application.service import StarterService

Session = Annotated[
    str,
    Header(alias="X-Session-Code", min_length=1, max_length=128),
]


class AddProgrammeItemRequest(BaseModel):
    film_code: str = Field(alias="filmCode")
    screening_count: StrictInt = Field(alias="screeningCount")


class UpdateProgrammeItemRequest(BaseModel):
    screening_count: StrictInt = Field(alias="screeningCount")


def routes(service: StarterService):
    router = APIRouter(prefix="/api")

    @router.get("/health")
    def health():
        if not service.health():
            raise HTTPException(503, "Database unavailable")
        return {"status": "ok", "database": "connected"}

    @router.get("/films")
    def films():
        return {"items": service.catalogue()}

    @router.get("/films/{film_code}")
    def film_detail(film_code: str):
        film = service.catalogue_item(film_code)
        if film is None:
            raise HTTPException(404, "Film not found")
        return film

    @router.post("/screening-programmes")
    def create_programme(session_code: Session):
        return service.create_programme(session_code)

    @router.get("/screening-programmes/{programme_code}")
    def get_programme(programme_code: str, session_code: Session):
        return service.get_programme(programme_code, session_code)

    @router.post("/screening-programmes/{programme_code}/items")
    def add_item(
        programme_code: str,
        body: AddProgrammeItemRequest,
        session_code: Session,
    ):
        return service.add_item(
            programme_code,
            session_code,
            body.film_code,
            body.screening_count,
        )

    @router.put(
        "/screening-programmes/{programme_code}/items/{film_code}"
    )
    def edit_item(
        programme_code: str,
        film_code: str,
        body: UpdateProgrammeItemRequest,
        session_code: Session,
    ):
        return service.edit_item(
            programme_code,
            session_code,
            film_code,
            body.screening_count,
        )

    @router.delete(
        "/screening-programmes/{programme_code}/items/{film_code}"
    )
    def remove_item(
        programme_code: str,
        film_code: str,
        session_code: Session,
    ):
        return service.remove_item(
            programme_code,
            session_code,
            film_code,
        )

    return router
