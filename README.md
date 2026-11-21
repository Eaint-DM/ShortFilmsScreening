# AA-02 S02 — Short-Film Screening Programme

## Project Overview

This application supports the S02 short-film screening programme. A film-club organiser can browse the seeded catalogue, inspect film details, and add, update, or remove films in a session-owned programme. The backend calculates total viewing time from each film's stored runtime and screening count.

## Group Members

The group members and their contribution areas are:

| Student ID | Name | Contribution area |
| --- | --- | --- |
| 6804860018  | Sai Thit Swan Thu  | Frontend implementation |
| 6704860018  | Eaint Myint Mon  | Backend business logic and API backend |
| 6704860010  | Lakshya Timsina Chhetri  | Database, Docker, integration and testing database |

## Technology Stack

Python 3.14, FastAPI, psycopg, PostgreSQL 18, vanilla JavaScript and Nginx. Docker Compose v2 is used to run the services. No Node build step is needed; Python dependencies are installed in the backend container.

## Setup Instructions

1. Install and start the class-approved Docker engine with Compose v2. Check `docker version` and `docker compose version`.
2. Open a terminal at this project root (the folder containing submission-manifest.yml).
3. Run `docker compose -f config/docker-compose.yml config` to verify resolved configuration.
4. Run the startup command below. Ports 8080 and 8000 must be free. Local development database credentials are in config/docker-compose.yml; do not use them for a public deployment.

**Local verification — 21 November 2026:** I verified the resolved configuration with `docker --context rancher-desktop compose -f config/docker-compose.yml config`. After `up --build -d`, `ps` showed the frontend and backend running and the database healthy. This run used an existing database volume; first-time SQL initialization was not retested.

The first startup initialises database/001-schema.sql and 002-seed.sql on a new Compose volume. Later edits to SQL files do not automatically update an existing database. Apply a reviewed migration, or use a fresh project name for a disposable development run. Do not remove a volume containing work you need.

## Run Instructions

```sh
docker --context rancher-desktop compose -f config/docker-compose.yml up --build -d
docker --context rancher-desktop compose -f config/docker-compose.yml ps
docker --context rancher-desktop compose -f config/docker-compose.yml logs backend database
```

Open http://127.0.0.1:8080. The page loads the film catalogue and initializes the current browser session's screening programme. Use **View details** on a film to see its information; use the screening-count field and **Add to programme** to add it. The programme supports updating counts and removing films, and displays the total returned by the backend. The **Developer Diagnostics** panel provides health and catalogue checks. API documentation is at http://127.0.0.1:8000/api/docs.

In Windows PowerShell, use `curl.exe` instead of `curl` to avoid the older alias.

```sh
curl --fail http://127.0.0.1:8080/api/health
curl --fail http://127.0.0.1:8080/api/films
curl --fail http://127.0.0.1:8000/api/films/FILM-001
docker --context rancher-desktop compose -f config/docker-compose.yml exec -T database psql -U postgres -d "film screening" -c "SELECT code, name, duration FROM catalogue_items;"
docker --context rancher-desktop compose -f config/docker-compose.yml down
```

`down` stops this project's services and keeps its database volume. Root `docker-compose.yml` and `docker-compose.mac.yml` include the same portable config for older command habits. Use one project name/config consistently; do not start multiple copies on the same ports.

## API Endpoints

| Method/path | Behaviour |
| --- | --- |
| GET /api/health | Checks PostgreSQL connectivity |
| GET /api/films | Lists the seeded short-film catalogue |
| GET /api/films/{filmCode} | Reads one film's details |
| POST /api/screening-programmes | Creates or returns the programme for X-Session-Code |
| GET /api/screening-programmes/{programmeCode} | Reads saved films and server-calculated total minutes |
| POST /api/screening-programmes/{programmeCode}/items | Adds a film with a screening count |
| PUT /api/screening-programmes/{programmeCode}/items/{filmCode} | Updates a film's screening count |
| DELETE /api/screening-programmes/{programmeCode}/items/{filmCode} | Removes a film from the programme |

Programme requests require the same non-empty `X-Session-Code`. Screening counts must be whole numbers from 1 through 3. The server calculates `totalMinutes` using the catalogue runtimes. Invalid counts return HTTP 400, duplicate additions return HTTP 409, and unknown or inaccessible films/programmes/items return HTTP 404. The session code is a mock ownership marker, not authentication.

## Known Limitations

The browser creates a new mock session code on page load; reloading the page does not resume a previous session's programme. The code is not authentication, and the application is a local S02 coursework project rather than a production service. Verify the member IDs and contribution records in `submission-manifest.yml`, and add any other sources or AI tools if they are used later.

The required integration, testing/debugging and contribution records are in `evidence/`. Review each member's attribution and ensure every claim reflects actual work. Acknowledge sources, libraries, examples and AI use, including incorporated output and how it was verified or modified. Keep screenshot and other evidence links relative to the document that references them.

Before submission, complete and verify the manifest and evidence, then follow [INSTRUCTION.md](INSTRUCTION.md) for the full workflow from group formation through Canvas upload.

## Local submission checker

Install the small checker dependency on the host: `python -m pip install -r config/checker-requirements.txt`. Python 3.10 or newer can run the checker independently of the Python 3.14 application container. Run from the project root:

```sh
python check_submission.py .
python check_submission.py /path/to/128-353-AA2-YourGroupID.zip
```

The ten C01-C10 lines correspond to the brief's ten submission artefact bullets. ZIP input adds A01 format and A02 filename/group matching. Every line is TRUE or FALSE with an actionable failure message. Exit status is 0 when all local checks pass and 1 when any check fails. ZIPs can contain the project at the archive root or within one enclosing project folder. The checker reads files only and never imports or executes submitted application code, startup commands or evidence scripts.

The untouched starter reports **C01-C10 all FALSE**. C01 checks required manifest fields and obvious placeholders. C02 and C07-C09 require every specified README/evidence heading to contain substantive, non-placeholder content; headings alone do not pass. C03-C05 require source or data beyond the unchanged distributed bootstrap. C06 requires configuration files plus a documented, actual setup/configuration verification result in the README Setup Instructions. A working configuration may be reused unchanged.

C10 requires completed evidence sections and checks referenced local Markdown links/images, reference-link definitions, HTML src/href attributes and single-backtick asset paths ending in common evidence extensions. Use links relative to each evidence file, for example `[Observed log](assets/request.log)` for `evidence/assets/request.log`. Angle brackets support linked filenames containing spaces. Remote web URLs and in-document fragments are not downloaded or verified. Local references must stay inside the submission; ZIP entries must use safe unique relative paths and cannot be symbolic links. Evidence can pass with **zero attachments** when its completed text has no local asset references.

These are local readiness heuristics based on file content and bundled bootstrap fingerprints. A changed file or TRUE result does not prove working integration, correct scenario calculations, complete or authentic observations, accurate contributions, source/AI acknowledgement quality, or an assessment grade. The checker never runs submitted code. Canvas upload and the Course Leader's confirmed deadline remain manual steps outside the automated results.

### Local submission checker details

The local submission checker `check_submission.py` uses these criteria:

| Check | Returns TRUE when |
|---|---|
| C01 Manifest | YAML is valid, required fields and artefact paths are correct, identity placeholders are replaced, and URLs have valid HTTP(S) form. |
| C02 README | Every required heading exists and contains non-empty, non-placeholder text. |
| C03 Frontend | Recognised, non-empty source files exist, and at least one is added or changed from the distributed starter. |
| C04 Backend | Same rule as C03, applied to backend/. |
| C05 Database | Recognised, non-empty data/schema/model files exist, with an addition or change from the starter. |
| C06 Configuration | Configuration files exist, and README Setup Instructions contains no placeholders and a verification word such as `tested`, `verified` or `passed`. Existing configuration may be reused. |
| C07 Integration evidence | Every required heading contains non-empty, non-placeholder text. |
| C08 Testing/debugging evidence | Same section-completion rule as C07. |
| C09 Contribution evidence | Same section-completion rule as C07. |
| C10 Referenced assets | All three evidence documents pass their section checks, and every recognised local asset reference resolves to a readable file inside the submission. Attachments are optional when evidence is inline. |

For ZIP input, it additionally checks:

- A01: readable ZIP, valid file integrity and safe archive structure.
- A02: filename exactly matches `128-353-AA2-<group.id>.zip`.

Placeholder detection includes TODO, TBD, FIXME and known template phrases. There is no minimum word count. Source comparisons ignore line-ending differences.

These are local heuristics. A changed file does not prove implemented functionality, and filled evidence sections do not prove authentic evidence. The checker does not run the application, validate scenario calculations, verify Canvas submission or award grades.