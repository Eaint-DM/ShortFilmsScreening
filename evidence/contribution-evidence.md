# Contribution Evidence

## Contribution Summary

**Contributor:** Eaint Myint Mon  
**Contribution area:** Backend business logic and API implementation  
**Work and verification date:** 21 November 2026

I implemented the server-side S02 screening-programme workflow in the backend. My work includes the FastAPI routes, application service, domain validation and calculation rules, persistence ports, PostgreSQL adapter, and database-independent service tests. I also reviewed the frontend/API route mismatch and added backend and documentation changes to align the API with the S02 UI.

My implementation work is in:

- `backend/app/presentation/api.py` and `backend/app/main.py` — health, catalogue, and screening-programme routes; HTTP status and error translation; application startup.
- `backend/app/application/service.py` — programme creation and retrieval, catalogue lookup, add/update/remove operations, session ownership checks, and duplicate/not-found handling.
- `backend/app/domain/scenario.py` — screening-count validation and calculation of programme duration from stored film runtimes.
- `backend/app/domain/ports.py` and `backend/app/infrastructure/postgres.py` — application data contracts and PostgreSQL persistence.
- `backend/tests/test_service.py` — service-level tests for catalogue fields, programme operations, validation, duplicate films, totals, and session ownership.
- `backend/README.md` — API route and local test documentation.

I verified this work against the FastAPI application, in-memory service tests, Docker-backed API responses, and the repository submission structure. The backend rejected invalid counts as HTTP 400 and returned the saved screening count and server-calculated total minutes for valid operations.



**Contributor:** Sai Thit Swan Thu  
**Contribution area:** Frontend implementation, frontend-to-API integration, browser workflow testing, and frontend/testing evidence  
**Work and verification date:** 21 November 2026

I implemented the S02 browser interface and connected its user actions to the existing screening-programme API. My implementation work is in:

- `frontend/index.html` — the page structure for the film catalogue, film details, screening programme, programme summary, and developer diagnostics.
- `frontend/assets/styles/main.css` — the visual layout and styling for the catalogue, film cards, programme entries, summary, and user feedback.
- `frontend/scripts/index.js` — catalogue loading, film-detail retrieval, mock-session programme initialization, add/update/remove actions, screening-count validation, queued programme operations, and success/error messages.

I used the existing `frontend/scripts/http.js` request helper and `frontend/scripts/action-queue.js` helper; these helper files were part of the project and are not claimed as my original implementation. The frontend calls the API through the same-origin `/api` path, sends the mock session code with programme requests, and refreshes the saved programme after mutations. The displayed programme total is taken from the API response rather than independently calculated as the authoritative value in the browser.

I also ran the four S02 browser/API evidence cases using the same mock session. The observed totals were 20 minutes after adding Next Floor and Alike once each, 32 minutes after changing Next Floor to two screenings, and 24 minutes after removing Alike. The invalid screening-count test returned HTTP 400 from the API and the subsequent GET confirmed that the saved count and 24-minute total were unchanged. Supporting screenshots are linked below and detailed in the testing evidence file.

I documented my testing/debugging work in `evidence/testing-debugging-evidence.md` and my frontend portion of the integration work in `evidence/integration-evidence.md`.

My relevant Git history is:

| Work | Branch / commit | Integration into `main` |
|---|---|---|
| S02 frontend implementation | `frontend/s02-screening-ui` — `2d7eac8` (`Complete S02 screening programme frontend`) | Pull Request #1, merged |
| Testing and debugging evidence | `evidence/c08-testing-debugging` — `7758e43` (`Add S02 testing and debugging evidence`) | Pull Request #2, merged |
| Frontend integration evidence | `evidence/c07-frontend-integration` — `3036471` (`Add S02 frontend integration evidence`) | Pull Request #3, merged |

The merged branch history is visible in the repository's `main` branch. The commit and pull-request references identify my changes; they do not claim authorship of the backend, database, or configuration implementation.

## Individual Contributions

**Sai Thit Swan Thu — Frontend and frontend evidence**

My individual work was to implement and verify the S02 frontend workflow. The specific files, activities, and evidence are:

- `frontend/index.html`, `frontend/assets/styles/main.css`, and `frontend/scripts/index.js` — implemented the S02 page and browser interactions.
- `frontend/scripts/http.js` and `frontend/scripts/action-queue.js` — reused the supplied helpers for API requests and ordered programme operations; I did not claim authorship of these helper files.
- `evidence/testing-debugging-evidence.md` — documented API requests, browser/network observations, the invalid-count issue, the frontend/backend rejection, and retest results.
- `evidence/integration-evidence.md` — documented my Integrated Workflow, Frontend Evidence, Success Case, and Error or Empty-Data Case sections. Backend API Evidence and Database Evidence are left for the responsible teammates.
- `evidence/screenshots/` — captured the browser and API evidence for the four S02 test cases.

The following screenshots provide examples of the work and its verification:

- [Catalogue and programme after adding both films](<screenshots/test-01-add-two-films-ui 6.17.03 AM.png>)
- [Programme API response after adding both films](<screenshots/test-01-add-two-films-get-response 6.17.18 AM.png>)
- [Updated programme after changing the screening count](<screenshots/test-02-update-count-ui 6.17.53 AM.png>)
- [Programme API response after updating the count](<screenshots/test-02-update-count-api-response 6.18.03 AM.png>)
- [Programme after removing Alike](<screenshots/test-03-remove-alike-ui 6.19.49 AM.png>)
- [Frontend validation for a zero screening count](<screenshots/test-04-frontend-validation 6.23.08 AM.png>)
- [Backend rejection and follow-up programme verification](<screenshots/test-04-backend-validation-and-verification 6.29.03 AM.png>)

**Eaint Myint Mon — backend business logic and API backend**

My individual work was to implement and verify the S02 backend workflow. The specific files and responsibilities are:

- `backend/app/presentation/api.py` and `backend/app/main.py` — exposed the health, film-catalogue, and screening-programme endpoints, translated request validation and service errors into HTTP responses, and assembled the application.
- `backend/app/application/service.py` — implemented programme creation and retrieval, film lookups, item add/update/remove operations, session ownership checks, and duplicate/not-found handling.
- `backend/app/domain/scenario.py` — implemented the screening-count rules (whole numbers from 1 through 3) and calculated programme duration from film runtimes and saved screening counts.
- `backend/app/domain/ports.py` and `backend/app/infrastructure/postgres.py` — defined the application’s data contracts and connected the workflow to the existing PostgreSQL catalogue and collections schema.
- `backend/tests/test_service.py` — added database-independent tests for catalogue response fields, programme creation, add/update/remove totals, invalid counts, duplicate films, and session ownership.
- `backend/README.md` — documented the API routes, local setup, architecture, and test command.

The service tests use in-memory fakes to verify business behaviour independently of PostgreSQL. The backend changes build on the project’s existing database schema and seeded film data.

**Reproducible verification — 21 November 2026**

From `backend/`, I ran:

```sh
python3 -m unittest discover -s tests
```

The observed result was `Ran 5 tests ... OK`. This verifies the database-independent service workflow, including the expected 20-minute add result, 32-minute update result, 24-minute remove result, unchanged state after invalid counts, and rejection of duplicate films or foreign sessions.

I also ran the Docker Compose application locally and checked the API/OpenAPI routes and service responses. Valid programme operations returned the saved items and server-calculated `totalMinutes`; an invalid screening count was rejected with HTTP 400. These results also exercised the existing PostgreSQL persistence adapter and seeded catalogue data.

**Endpoint verification — 21 November 2026**

The following commands were used or reproduced for the locally running application. For programme commands, replace `<mock-session-code>` with the same non-empty `X-Session-Code` value used for every request in that session. `PRG-732f97ef27b3476d9ef20e41b5bdc03a` is the programme code recorded in the testing evidence.

| Endpoint and command | Observed or implementation-defined result |
|---|---|
| **Health check**<br>`curl -i http://127.0.0.1:8080/api/health` | Implemented database connectivity check. A successful response is HTTP 200 with `{"status":"ok","database":"connected"}`. |
| **Load catalogue**<br>`curl -i http://127.0.0.1:8080/api/films` | Catalogue request was observed successfully; the frontend loaded the seeded films. |
| **Load one film**<br>`curl -i http://127.0.0.1:8080/api/films/FILM-001` | Retrieved the FILM-001 record. Unknown codes are implemented to return HTTP 404. |
| **Create or retrieve programme**<br>`curl -i -X POST http://127.0.0.1:8080/api/screening-programmes -H "X-Session-Code: <mock-session-code>"` | Returned HTTP 200 and a `programmeCode` for the mock session. The testing evidence used `PRG-732f97ef27b3476d9ef20e41b5bdc03a`. |
| **Retrieve programme**<br>`curl -i http://127.0.0.1:8080/api/screening-programmes/PRG-732f97ef27b3476d9ef20e41b5bdc03a -H "X-Session-Code: <mock-session-code>"` | Verified HTTP 200 after add, update, remove, and invalid-update operations. The successful states returned `totalMinutes` of 20, 32, and 24 respectively. |
| **Add FILM-001**<br>`curl -i -X POST http://127.0.0.1:8080/api/screening-programmes/PRG-732f97ef27b3476d9ef20e41b5bdc03a/items -H "X-Session-Code: <mock-session-code>" -H "Content-Type: application/json" -d '{"filmCode":"FILM-001","screeningCount":1}'` | HTTP 200 and returned the saved programme with FILM-001 at count 1 and `totalMinutes: 12`. |
| **Add FILM-002**<br>`curl -i -X POST http://127.0.0.1:8080/api/screening-programmes/PRG-732f97ef27b3476d9ef20e41b5bdc03a/items -H "X-Session-Code: <mock-session-code>" -H "Content-Type: application/json" -d '{"filmCode":"FILM-002","screeningCount":1}'` | HTTP 200 and returned both saved entries with `totalMinutes: 20`. Readding the same film is implemented to return HTTP 409. |
| **Update screening count**<br>`curl -i -X PUT http://127.0.0.1:8080/api/screening-programmes/PRG-732f97ef27b3476d9ef20e41b5bdc03a/items/FILM-001 -H "X-Session-Code: <mock-session-code>" -H "Content-Type: application/json" -d '{"screeningCount":2}'` | HTTP 200 and returned FILM-001 at count 2, FILM-002 at count 1, and `totalMinutes: 32`. |
| **Reject invalid count**<br>`curl -i -X PUT http://127.0.0.1:8080/api/screening-programmes/PRG-732f97ef27b3476d9ef20e41b5bdc03a/items/FILM-001 -H "X-Session-Code: <mock-session-code>" -H "Content-Type: application/json" -d '{"screeningCount":0}'` | HTTP 400 with `error_code: INVALID_REQUEST` and `screening_count must be between 1 and 3`. The follow-up programme GET showed FILM-001 unchanged at count 2 and `totalMinutes: 24`. |
| **Remove FILM-002**<br>`curl -i -X DELETE http://127.0.0.1:8080/api/screening-programmes/PRG-732f97ef27b3476d9ef20e41b5bdc03a/items/FILM-002 -H "X-Session-Code: <mock-session-code>"` | HTTP 200 and returned only FILM-001 at count 2 and `totalMinutes: 24`. Unknown or inaccessible programmes/items are implemented to return HTTP 404. |

My relevant Git history is:

| Work | Commit |
|---|---|
| Screening-count validation and duration calculation | `140396f` (`feat: implement screening validation and duration calculation`) |
| S02 application service, API, and persistence integration | `6c483dd` (`feat: implement S02 screening programme API`) |
| Screening-programme service tests | `7b40f5a` (`test: cover S02 screening programme workflows`) |
| Backend API documentation | `3c70b67` (`docs: document S02 backend API`) |

**Lakshya Timsina Chhetri:**
`Database`

* Adapted `database/001-schema.sql` for the screening-programme data model:
  catalogue films, session-owned programmes, and programme-film entries.
* Defined the table keys and foreign-key relationships, including the
  composite key that prevents duplicate film entries in a programme.
* Added database constraints for valid film years and positive runtimes, and
  for screening counts from 1 to 3 inclusive.
* Updated `database/002-seed.sql` with 20 film catalogue records, including
  each film's code, title, year, genre, runtime, director, description, and URL researched and picked from the vemio catalogue.
* Checked the schema and seed definitions against the S02 requirements and
  confirmed that Docker Compose mounts both SQL files for database
  initialization.

## Research or Technology Decisions

**By Eaint Myint Mon**

I used the existing FastAPI, psycopg, and PostgreSQL architecture because it matched the supplied project structure and avoided adding an unnecessary framework or service. The backend is organised into presentation, application, domain, and infrastructure layers:

- `backend/app/presentation/` exposes HTTP routes and translates application outcomes into API responses.
- `backend/app/application/service.py` coordinates the S02 workflow and keeps persistence details behind the repository interfaces.
- `backend/app/domain/scenario.py` owns the screening-count bounds and server-calculated duration rule.
- `backend/app/infrastructure/postgres.py` implements the persistence contract for PostgreSQL.

I researched and tested the mismatch between the supplied frontend requests and the S02 backend paths. I traced the route names through `frontend/scripts/index.js`, `backend/app/presentation/api.py`, and the FastAPI documentation, then used the existing `/api/screening-programmes` resource shape rather than introducing separate endpoints or a different session mechanism.

The mock session code remains the existing `X-Session-Code` header described by the starter and scenario. I retained this approach because it provides repeatable local ownership isolation without presenting it as authentication. Screening counts are validated as whole numbers from 1 through 3, and totals are calculated by the backend from saved counts and catalogue runtimes so that the browser does not become the authority for the final result.

I chose database-independent service tests with in-memory fakes for the domain/application behaviour. PostgreSQL-backed route checks and Docker Compose runs were used separately to verify persistence and HTTP integration.

**By Sai Thit Swan Thu**

For my frontend work, I followed the S02 workflow and the existing project structure rather than introducing a separate frontend framework or build system. The interface uses the project's existing vanilla JavaScript setup and browser APIs.

I reused the supplied request helper so frontend calls use the same-origin `/api` proxy and so programme requests can include the `X-Session-Code` header. I reused the supplied action-queue helper to serialize programme operations. After each add, update, or remove operation, the frontend retrieves the saved programme and displays the returned entries and `totalMinutes`; this avoids presenting a separately calculated browser total as the authoritative saved result.

The screening-count input is constrained to whole-number values from 1 to 3 in the interface, with visible feedback for invalid input. I also checked the server-side validation separately because client-side validation alone does not demonstrate that an invalid request is rejected by the API.

The scenario requirements in `aa-02-s02.md` were used as the reference for the film and screening-programme workflow. No additional third-party frontend library was introduced for my implementation.


## Academic Integrity and Source Acknowledgement

**By Sai Thit Swan Thu**
**Project and technical sources used:**

- `aa-02-s02.md` — the supplied S02 scenario and workflow requirements.
- [Vimeo short-film search](https://vimeo.com/search?q=short%20films) — used as a source for short-film catalogue information.
- The existing project frontend files, including `frontend/scripts/http.js` and `frontend/scripts/action-queue.js`, which I reused rather than claiming as my own work.
- The running project's API responses and browser observations, which I used to verify the frontend behaviour.
- Browser-provided APIs such as `fetch`, DOM APIs, and `crypto.randomUUID`; no separate third-party frontend library was added for this work.

**AI assistance disclosure — Lakshya Timsina Chhetri:** On 21 November 2026, Lakshya used GitHub Copilot in VS Code (Copilot SDK) to add the JSON-formatted information to the seed data. Copilot-assisted seed changes were reviewed against the project schema and the resulting catalogue records were checked through the database-backed application.

**AI assistance disclosure — Sai Thit Swan Thu:** On 21 November 2026, Sai used ChatGPT (OpenAI) as a development aid for explanations, frontend code drafting/revision guidance, troubleshooting, Git workflow guidance, and drafting/reviewing the C07 and C08 evidence text. Sai reviewed and adapted the suggestions to the actual project files, then ran the application locally, exercised the browser workflow, checked API responses and validation behaviour, captured screenshots, and ran the submission checker. The recorded test outcomes and screenshots are observations from the local project; they were not generated by the AI tool.

**AI assistance disclosure — Eaint Myint Mon:** On 21 November 2026, Eaint used GitHub Copilot in VS Code (Copilot SDK) for repository inspection, API/frontend troubleshooting, Git workflow guidance, and documentation drafting. Copilot helped identify the mismatch between the starter UI and S02 API routes. An alternate UI draft was discarded; the retained Screening Studio UI came from the existing GitHub frontend branch. Copilot-assisted documentation was reviewed against the repository and observed local Compose, API, browser, and database results. 

**Verification tools used:** Visual Studio Code, Git/GitHub, Docker Compose, a web browser, browser Developer Tools (including Network and Console), and the project's `check_submission.py` checker.

