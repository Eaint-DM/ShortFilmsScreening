
"""Pure business rules for the S02 screening programme.

This module has no dependencies on HTTP, PostgreSQL,
or other application layers.
"""


def validate_entry(entry: dict) -> None:
    """Validate the screening count of a programme item."""

    if not isinstance(entry, dict):
        raise ValueError("Programme item must be an object.")

    if "screening_count" not in entry:
        raise ValueError("screening_count is required.")

    count = entry["screening_count"]

    if type(count) is not int:
        raise ValueError("screening_count must be a whole number.")

    if not 1 <= count <= 3:
        raise ValueError(
            "screening_count must be between 1 and 3."
        )


def calculate_result(
    saved_entries: list[dict],
    stored_catalogue: list[dict],
) -> int:
    """Calculate total programme duration in minutes."""

    films_by_code = {
        film["film_code"]: film
        for film in stored_catalogue
    }

    total_minutes = 0

    for entry in saved_entries:
        validate_entry(entry)

        film_code = entry.get("film_code")

        if not isinstance(film_code, str) or not film_code:
            raise ValueError("A valid film_code is required.")

        film = films_by_code.get(film_code)

        if film is None:
            raise ValueError(
                f"Film {film_code} does not exist in the catalogue."
            )

        runtime = film.get("runtime_minutes")

        if type(runtime) is not int or runtime <= 0:
            raise ValueError(
                f"Invalid runtime for film {film_code}."
            )

        total_minutes += runtime * entry["screening_count"]

    return total_minutes
