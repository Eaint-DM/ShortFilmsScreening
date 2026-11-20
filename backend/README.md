# Backend

The backend implements the S02 short-film screening programme API. Run it with
the project Compose configuration from the project root:

```sh
docker compose -f config/docker-compose.yml up --build -d
```

The API is available at `http://127.0.0.1:8000`; OpenAPI documentation is at
`http://127.0.0.1:8000/api/docs`.

## Routes

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/films` | List the seeded film catalogue |
| GET | `/api/films/{filmCode}` | Read one film |
| POST | `/api/screening-programmes` | Create or return the session's programme |
| GET | `/api/screening-programmes/{programmeCode}` | Read saved films and total minutes |
| POST | `/api/screening-programmes/{programmeCode}/items` | Add a film with `filmCode` and `screeningCount` |
| PUT | `/api/screening-programmes/{programmeCode}/items/{filmCode}` | Change `screeningCount` |
| DELETE | `/api/screening-programmes/{programmeCode}/items/{filmCode}` | Remove a saved film |

Send the same non-empty `X-Session-Code` header on every programme request.
It is a mock ownership marker, not authentication. Programme reads and
mutations are scoped by both programme code and session code; an inaccessible
programme is reported as not found.

Counts must be strict whole numbers from 1 through 3. The backend calculates
`totalMinutes` from the saved counts and catalogue runtimes in PostgreSQL.
Duplicate additions return HTTP 409; invalid counts return HTTP 400; unknown
films, programmes, or saved items return HTTP 404. The adapter uses the
existing `collections` and `collection_entries` schema and writes
`screeningCount` to its `entry_value` column.

## Layering and tests

`presentation/api.py` translates HTTP requests, `application/service.py`
coordinates use cases and result calculation, `domain/` contains the port
contracts and pure rules, and `infrastructure/postgres.py` implements both
database ports. `main.py` is the composition root.

Run the database-independent service and domain tests from `backend/`:

```sh
python -m unittest discover -s tests
```
