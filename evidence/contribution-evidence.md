# Contribution Evidence

Template only: no student implementation or completed evidence is supplied. Replace every TODO with actual observations. Include only assets you reference, using local relative links.

## Contribution Summary

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
<<<<<<< Updated upstream
=======

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

## Research or Technology Decisions

**By Sai Thit Swan Thu**

For my frontend work, I followed the S02 workflow and the existing project structure rather than introducing a separate frontend framework or build system. The interface uses the project's existing vanilla JavaScript setup and browser APIs.

I reused the supplied request helper so frontend calls use the same-origin `/api` proxy and so programme requests can include the `X-Session-Code` header. I reused the supplied action-queue helper to serialize programme operations. After each add, update, or remove operation, the frontend retrieves the saved programme and displays the returned entries and `totalMinutes`; this avoids presenting a separately calculated browser total as the authoritative saved result.

The screening-count input is constrained to whole-number values from 1 to 3 in the interface, with visible feedback for invalid input. I also checked the server-side validation separately because client-side validation alone does not demonstrate that an invalid request is rejected by the API.

The scenario requirements in `aa-02-s02.md` were used as the reference for the film and screening-programme workflow. No additional third-party frontend library was introduced for my implementation.

**By Lakshya Timsina Chetri**
`Database`
>>>>>>> Stashed changes

My individual work was to implement and verify the S02 frontend workflow. The specific files, activities, and evidence are:

<<<<<<< Updated upstream
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

## Research or Technology Decisions

**By Sai Thit Swan Thu**

For my frontend work, I followed the S02 workflow and the existing project structure rather than introducing a separate frontend framework or build system. The interface uses the project's existing vanilla JavaScript setup and browser APIs.

I reused the supplied request helper so frontend calls use the same-origin `/api` proxy and so programme requests can include the `X-Session-Code` header. I reused the supplied action-queue helper to serialize programme operations. After each add, update, or remove operation, the frontend retrieves the saved programme and displays the returned entries and `totalMinutes`; this avoids presenting a separately calculated browser total as the authoritative saved result.

The screening-count input is constrained to whole-number values from 1 to 3 in the interface, with visible feedback for invalid input. I also checked the server-side validation separately because client-side validation alone does not demonstrate that an invalid request is rejected by the API.

The scenario requirements in `aa-02-s02.md` were used as the reference for the film and screening-programme workflow. No additional third-party frontend library was introduced for my implementation.

=======
>>>>>>> Stashed changes
## Academic Integrity and Source Acknowledgement

**By Sai Thit Swan Thu**
**Project and technical sources used:**

- `aa-02-s02.md` — the supplied S02 scenario and workflow requirements.
- The existing project frontend files, including `frontend/scripts/http.js` and `frontend/scripts/action-queue.js`, which I reused rather than claiming as my own work.
- The running project's API responses and browser observations, which I used to verify the frontend behaviour.
- Browser-provided APIs such as `fetch`, DOM APIs, and `crypto.randomUUID`; no separate third-party frontend library was added for this work.

**AI assistance disclosure:** On 21 November 2026, I used ChatGPT (OpenAI) as a development aid for explanations, frontend code drafting/revision guidance, troubleshooting, Git workflow guidance, and drafting/reviewing the C07 and C08 evidence text. I reviewed and adapted the suggestions to the actual project files. I then ran the application locally, exercised the browser workflow, checked the API responses and validation behaviour, captured the screenshots, and ran the submission checker. The recorded test outcomes and screenshots are observations from my local project; they were not generated by the AI tool. The AI assistance is acknowledged here rather than presented as independent student work.

**Verification tools used:** Visual Studio Code, Git/GitHub, Docker Compose, a web browser, browser Developer Tools (including Network and Console), and the project's `check_submission.py` checker.

