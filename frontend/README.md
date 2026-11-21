# Frontend

Nginx serves this directory, and `config/nginx.conf` proxies same-origin `/api/` requests to the backend. See the [project README](../README.md) for Compose setup and run instructions.

## S02 workflow

When the page opens, `scripts/index.js` loads the film catalogue and creates or retrieves a screening programme for a mock browser session. The user can:

- browse films and open a film's details;
- add a film with a screening count from 1 to 3;
- update a saved film's screening count or remove that film;
- view the programme total returned by the backend.

Programme operations send the same `X-Session-Code` during the current page load and use `scripts/action-queue.js` to keep reads and writes ordered. After a mutation, the frontend retrieves the saved programme and renders the server response; JavaScript does not calculate the authoritative total. The developer diagnostics panel exposes health and catalogue checks. Its generic collection test is disabled for this S02 implementation.

## Runtime and files

The frontend is static HTML, CSS and JavaScript; there is no Node build step. The Compose frontend service mounts this directory into Nginx. The main entry point is `index.html`; `scripts/http.js` provides same-origin API requests.

The mock session code changes on page reload. Reload persistence and authentication are outside this coursework scenario.
