
"""Domain ports defining the operations required by the application."""
from typing import Protocol


class DataPort(Protocol):
    """Read-only access to the seeded film catalogue."""

    def health(self) -> bool: ...
    def catalogue(self) -> list[dict]: ...
    def catalogue_item(self, film_code: str) -> dict | None: ...


class CollectionPort(Protocol):
    """Persistence operations for session-owned screening programmes."""

    def create_or_get(self, session_code: str) -> dict: ...

    def read(
        self, programme_code: str, session_code: str
    ) -> dict | None: ...

    def add(
        self, programme_code: str, session_code: str, entry: dict
    ) -> bool: ...

    def edit(
        self,
        programme_code: str,
        session_code: str,
        film_code: str,
        entry: dict,
    ) -> bool: ...

    def remove(
        self, programme_code: str, session_code: str, film_code: str
    ) -> bool: ...
