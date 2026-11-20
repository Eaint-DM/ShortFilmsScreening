
"""Application services implementing the screening programme workflow."""

from app.domain.ports import DataPort, CollectionPort
from app.domain.scenario import validate_entry, calculate_result


class ValidationError(Exception):
    pass


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class StarterService:
    def __init__(self, data: DataPort, collections: CollectionPort):
        self.data = data
        self.collections = collections

    def health(self):
        return self.data.health()

    def catalogue(self):
        return [self._film_response(film) for film in self.data.catalogue()]

    def catalogue_item(self, film_code: str):
        film = self.data.catalogue_item(film_code)
        return self._film_response(film) if film is not None else None

    def create_programme(self, session_code: str):
        programme = self.collections.create_or_get(session_code)
        return {"programmeCode": programme["programme_code"]}

    def get_programme(self, programme_code: str, session_code: str):
        programme = self.collections.read(programme_code, session_code)
        if programme is None:
            raise NotFoundError("Screening programme not found.")

        films = self.data.catalogue()
        entries = programme.get("items", [])
        total_minutes = calculate_result(
            entries,
            [
                {
                    "film_code": film["code"],
                    "runtime_minutes": film["duration"],
                }
                for film in films
            ],
        )
        films_by_code = {film["code"]: film for film in films}

        return {
            "programmeCode": programme_code,
            "items": [
                {
                    "filmCode": item["film_code"],
                    "title": films_by_code[item["film_code"]]["name"],
                    "runtimeMinutes": films_by_code[item["film_code"]][
                        "duration"
                    ],
                    "genre": films_by_code[item["film_code"]]["genre"],
                    "screeningCount": item["screening_count"],
                }
                for item in entries
            ],
            "totalMinutes": total_minutes,
        }

    def add_item(
        self, programme_code: str, session_code: str, film_code: str,
        screening_count: int,
    ):
        self._validate_item(film_code, screening_count)
        self._require_owned_programme(programme_code, session_code)
        created = self.collections.add(
            programme_code,
            session_code,
            {
                "film_code": film_code,
                "screening_count": screening_count,
            },
        )
        if not created:
            if self.collections.read(programme_code, session_code) is None:
                raise NotFoundError("Screening programme not found.")
            raise ConflictError("Film is already in the screening programme.")
        return self.get_programme(programme_code, session_code)

    def edit_item(
        self, programme_code: str, session_code: str, film_code: str,
        screening_count: int,
    ):
        self._validate_item(film_code, screening_count)
        self._require_owned_programme(programme_code, session_code)
        updated = self.collections.edit(
            programme_code,
            session_code,
            film_code,
            {"screening_count": screening_count},
        )
        if not updated:
            raise NotFoundError("Programme item not found.")
        return self.get_programme(programme_code, session_code)

    def remove_item(
        self, programme_code: str, session_code: str, film_code: str,
    ):
        self._require_owned_programme(programme_code, session_code)
        removed = self.collections.remove(
            programme_code, session_code, film_code
        )
        if not removed:
            raise NotFoundError("Programme item not found.")
        return self.get_programme(programme_code, session_code)

    def _require_owned_programme(
        self, programme_code: str, session_code: str
    ) -> None:
        if self.collections.read(programme_code, session_code) is None:
            raise NotFoundError("Screening programme not found.")

    def _validate_item(self, film_code: str, screening_count: int):
        if self.data.catalogue_item(film_code) is None:
            raise NotFoundError("Film not found.")
        try:
            validate_entry(
                {
                    "film_code": film_code,
                    "screening_count": screening_count,
                }
            )
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc

    @staticmethod
    def _film_response(film: dict) -> dict:
        return {
            "filmCode": film["code"],
            "title": film["name"],
            "runtimeMinutes": film["duration"],
            "genre": film["genre"],
            "year": film["year"],
            "director": film["director"],
            "description": film["description"],
            "filmUrl": film["film_url"],
        }
