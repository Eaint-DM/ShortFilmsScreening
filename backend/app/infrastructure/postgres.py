"""Replaceable database driver; no dependencies on other project layers."""
from uuid import uuid4

import psycopg
from psycopg.rows import dict_row


class PostgresData:
    def __init__(self, url: str):
        self.url = url

    def _read(self, sql: str, values: tuple = ()) -> list[dict]:
        with psycopg.connect(
            self.url, row_factory=dict_row, connect_timeout=3
        ) as connection:
            return connection.execute(sql, values).fetchall()

    def health(self) -> bool:
        return self._read("SELECT 1 AS connected") == [{"connected": 1}]

    def catalogue(self) -> list[dict]:
        return self._read(
            "SELECT code, name, year, genre, duration, director, "
            "description, film_url FROM catalogue_items ORDER BY code"
        )

    def catalogue_item(self, code: str) -> dict | None:
        rows = self._read(
            "SELECT code, name, year, genre, duration, director, "
            "description, film_url FROM catalogue_items WHERE code = %s",
            (code,),
        )
        return rows[0] if rows else None

    def create_or_get(self, session_code: str) -> dict:
        rows = self._read(
            """
            INSERT INTO collections (code, session_code)
            VALUES (%s, %s)
            ON CONFLICT (session_code)
            DO UPDATE SET session_code = EXCLUDED.session_code
            RETURNING code
            """,
            (f"PRG-{uuid4().hex}", session_code),
        )
        return {"programme_code": rows[0]["code"]}

    def read(self, programme_code: str, session_code: str) -> dict | None:
        rows = self._read(
            """
            SELECT c.code AS programme_code,
                   e.item_code AS film_code,
                   e.entry_value AS screening_count
            FROM collections AS c
            LEFT JOIN collection_entries AS e
              ON e.collection_code = c.code
            WHERE c.code = %s AND c.session_code = %s
            ORDER BY e.item_code
            """,
            (programme_code, session_code),
        )
        if not rows:
            return None

        return {
            "programme_code": rows[0]["programme_code"],
            "items": [
                {
                    "film_code": row["film_code"],
                    "screening_count": row["screening_count"],
                }
                for row in rows
                if row["film_code"] is not None
            ],
        }

    def add(
        self, programme_code: str, session_code: str, entry: dict
    ) -> bool:
        rows = self._read(
            """
            INSERT INTO collection_entries
                (collection_code, item_code, entry_value)
            SELECT c.code, %s, %s
            FROM collections AS c
            WHERE c.code = %s AND c.session_code = %s
            ON CONFLICT (collection_code, item_code) DO NOTHING
            RETURNING collection_code
            """,
            (
                entry["film_code"],
                entry["screening_count"],
                programme_code,
                session_code,
            ),
        )
        return bool(rows)

    def edit(
        self,
        programme_code: str,
        session_code: str,
        film_code: str,
        entry: dict,
    ) -> bool:
        rows = self._read(
            """
            UPDATE collection_entries AS e
            SET entry_value = %s
            FROM collections AS c
            WHERE e.collection_code = c.code
              AND c.code = %s
              AND c.session_code = %s
              AND e.item_code = %s
            RETURNING e.collection_code
            """,
            (
                entry["screening_count"],
                programme_code,
                session_code,
                film_code,
            ),
        )
        return bool(rows)

    def remove(
        self, programme_code: str, session_code: str, film_code: str
    ) -> bool:
        rows = self._read(
            """
            DELETE FROM collection_entries AS e
            USING collections AS c
            WHERE e.collection_code = c.code
              AND c.code = %s
              AND c.session_code = %s
              AND e.item_code = %s
            RETURNING e.collection_code
            """,
            (programme_code, session_code, film_code),
        )
        return bool(rows)