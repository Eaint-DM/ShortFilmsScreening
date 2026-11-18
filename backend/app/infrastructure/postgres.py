"""Replaceable database driver; no dependencies on other project layers."""
import psycopg
from psycopg.rows import dict_row

class PostgresData:
    def __init__(self, url: str):
        self.url = url

    def _read(self, sql: str, values: tuple = ()) -> list[dict]:
        with psycopg.connect(self.url, row_factory=dict_row, connect_timeout=3) as connection:
            return connection.execute(sql, values).fetchall()

    def health(self) -> bool:
        return self._read("SELECT 1 AS connected") == [{"connected": 1}]

    def catalogue(self) -> list[dict]:
        return self._read(
            "SELECT code, name, year, genre, duration, director, description, film_url "
            "FROM catalogue_items ORDER BY code"
        )

    def catalogue_item(self, code: str) -> dict | None:
        rows = self._read(
            "SELECT code, name, year, genre, duration, director, description, film_url "
            "FROM catalogue_items WHERE code = %s",
            (code,),
        )
        return rows[0] if rows else None
    
    # TODO: parameterised, transactional collection persistence operations.
    def screening_count(self, collection_code: str) -> int:
        row = self._read(
            "SELECT COUNT(*) AS count FROM collection_entries WHERE collection_code = %s",
            (collection_code,)
        )
        return row[0]["count"] if row else 0

    # Enforce session ownership in every query, validate before mutations,
    def add_collection_entry(self, collection_code: str, item_code: str, entry_value: int):
        return self._read("INSERT INTO collection_entries (collection_code, item_code, entry_value) VALUES (%s, %s, %s) RETURNING collection_code, item_code", (collection_code, item_code, entry_value))
    # and DELETE only an entry, never its seeded catalogue record.
    def delete_collection(self, code: str):
        return self._read("DELETE FROM collections WHERE code = %s RETURNING code", (code,))