# Integration Evidence

Template only: no student implementation or completed evidence is supplied. Replace every TODO with actual observations. Include only assets you reference, using local relative links.

## Integrated Workflow

**Sai Thit Swan Thu role and test date:** I implemented and exercised the browser-facing screening-programme workflow on 21 November 2026 using the local application at `http://127.0.0.1:8080`.

**Reproduction steps from the frontend:**

1. Start the application from the project root with `docker compose -f config/docker-compose.yml up --build -d --wait`, then open `http://127.0.0.1:8080` in a browser.
2. Allow the page to load the film catalogue. The frontend requests the film list through the same-origin `/api` path and displays the returned films.
3. Select **View details** on a film. The frontend requests that film's details and displays the returned information.
4. Use the screening-programme controls. The page creates or retrieves a programme for its mock session and includes the session code on programme requests.
5. Add Next Floor (`FILM-001`, 12 minutes) and Alike (`FILM-002`, 8 minutes), each with a screening count of 1.
6. Change the screening count for Next Floor to 2, then remove Alike.
7. Observe the programme entries and total displayed by the browser after each operation.

**Expected result:** The browser programme should show the films and screening counts selected by the user, and the displayed total should reflect the latest saved programme after each operation.

**Observed result:** The browser showed both films and 20 minutes after the additions; Next Floor × 2 and Alike × 1 with 32 minutes after the update; and only Next Floor × 2 with 24 minutes after Alike was removed. The corresponding browser states are recorded in the [add](<screenshots/test-01-add-two-films-ui 6.17.03 AM.png>), [update](<screenshots/test-02-update-count-ui 6.17.53 AM.png>) and [remove](<screenshots/test-03-remove-alike-ui 6.19.49 AM.png>) screenshots.

## Frontend Evidence

**Sai Thit Swan Thu's implementation:** I implemented the S02 page structure and frontend behaviour in these files:

- `frontend/index.html` — page structure for the film catalogue, film details, screening programme, programme summary and developer diagnostics.
- `frontend/assets/styles/main.css` — styling for the screening application, film cards, programme entries, summary and user feedback.
- `frontend/scripts/index.js` — film loading and display, film-detail selection, session programme initialization, programme actions, validation, and success/error messages.

The frontend uses the existing `frontend/scripts/http.js` request helper to call the API through the `/api` proxy. It also uses the existing `frontend/scripts/action-queue.js` helper to sequence programme operations. The page creates a mock session code for the current browser page and sends it with programme requests. The interface supports adding a film, changing its screening count and removing it from the programme. After a programme mutation, the frontend retrieves the programme again and displays the returned entries and `totalMinutes`; it does not calculate the authoritative total in the browser.

The screening-count input is restricted in the interface to whole-number values from 1 to 3. An invalid value is rejected with visible feedback. The browser evidence for the implemented interface is: [catalogue and programme after adding films](<screenshots/test-01-add-two-films-ui 6.17.03 AM.png>), [updated programme](<screenshots/test-02-update-count-ui 6.17.53 AM.png>), [programme after removal](<screenshots/test-03-remove-alike-ui 6.19.49 AM.png>) and [invalid-input feedback](<screenshots/test-04-frontend-validation 6.23.08 AM.png>).

## Backend API Evidence

TODO: Record your actual work, date, reproducible steps, expected and observed results, and relevant supporting evidence.

## Database Evidence

TODO: Record your actual work, date, reproducible steps, expected and observed results, and relevant supporting evidence.

## Success Case

**Test date:** 21 November 2026.

**By Sai Thit Swan Thu:**
I used the browser interface to exercise the successful add, update and remove actions in the same screening programme.

| Action | Expected result | Observed browser result |
|---|---|---|
| Add Next Floor (`FILM-001`, 12 minutes) once and Alike (`FILM-002`, 8 minutes) once. | Two programme entries and a total of 20 minutes. | Both films appeared, each with one screening; total displayed as 20 minutes. [Browser evidence](<screenshots/test-01-add-two-films-ui 6.17.03 AM.png>) and [programme response evidence](<screenshots/test-01-add-two-films-get-response 6.17.18 AM.png>). |
| Change Next Floor to two screenings. | Next Floor × 2 and Alike × 1, for 32 minutes. | The programme displayed the updated count and a total of 32 minutes. [Browser evidence](<screenshots/test-02-update-count-ui 6.17.53 AM.png>) and [response evidence](<screenshots/test-02-update-count-api-response 6.18.03 AM.png>). |
| Remove Alike. | Only Next Floor × 2 remains, for 24 minutes. | Alike disappeared; Next Floor remained at two screenings and the total displayed as 24 minutes. [Browser evidence](<screenshots/test-03-remove-alike-ui 6.19.49 AM.png>) and [programme response evidence](<screenshots/test-03-remove-alike-get-response 6.20.01 AM.png>). |

The observed values matched the expected runtime totals: `12 × 1 + 8 × 1 = 20`, `12 × 2 + 8 × 1 = 32`, and `12 × 2 = 24` minutes.

## Error or Empty-Data Case

**Test date:** 21 November 2026.

**By Sai Thit Swan Thu:**
I tested the invalid screening-count case after the programme had reached the successful remove state, where Next Floor (`FILM-001`) remained at two screenings and the displayed total was 24 minutes.

1. Enter `0` as the screening count for Next Floor in the frontend.
2. Attempt the update.
3. Observe the frontend validation feedback and check the programme display.
4. To check the server-side rejection separately from the client-side validation, I also sent a direct `PUT` request from the browser Developer Tools Console using the same programme session and a body containing `{"screeningCount":0}`.
5. Retrieve the programme again and check that the rejected update did not change the saved state.

**Expected result:** A screening count of 0 is invalid. The interface should show an error, and the existing programme should remain unchanged.

**Observed result:** The frontend displayed a validation error and kept the total at 24 minutes. The direct request returned HTTP 400 with `error_code: INVALID_REQUEST` and the message `screening_count must be between 1 and 3`. The subsequent programme GET returned HTTP 200 and showed only `FILM-001` with a screening count of 2 and a total of 24 minutes. Evidence: [frontend validation feedback](<screenshots/test-04-frontend-validation 6.23.08 AM.png>) and [direct invalid request plus verification result](<screenshots/test-04-backend-validation-and-verification 6.29.03 AM.png>).
