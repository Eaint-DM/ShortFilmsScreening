# Testing and Debugging Evidence

The S02 screening-programme workflow was tested on 21 November 2026 using the locally running application at `http://127.0.0.1:8080`. The browser accessed the API through the frontend's same-origin `/api` proxy. The same mock session was retained for all programme operations. The evidence below records the browser state, API responses, validation behaviour and retest results.

## API Request Evidence

The following S02 API requests were exercised. Programme requests used the same `X-Session-Code` header so that each request operated on the same session programme.

| Purpose | Method and path | Input / expected result | Observed result |
|---|---|---|---|
| Load the film catalogue | `GET /api/films` | Return the seeded film catalogue. | The catalogue loaded and the frontend displayed the available films. |
| Create or retrieve the session programme | `POST /api/screening-programmes` | Send the session header and receive a `programmeCode`. | The programme was initialized and then used for the following requests. |
| Add the two test films | `POST /api/screening-programmes/{programmeCode}/items` | Add `FILM-001` with `{"filmCode":"FILM-001","screeningCount":1}` and `FILM-002` with `{"filmCode":"FILM-002","screeningCount":1}`. | The following programme GET returned both saved entries and `totalMinutes: 20`. |
| Retrieve the saved programme | `GET /api/screening-programmes/{programmeCode}` | Return saved entries, screening counts and the server-calculated total. | The response showed Next Floor (12 minutes) × 1, Alike (8 minutes) × 1, and `totalMinutes: 20`. |
| Update Next Floor | `PUT /api/screening-programmes/{programmeCode}/items/FILM-001` | Send `{"screeningCount":2}` and retrieve the programme again. | The update succeeded; the following GET showed counts 2 and 1 and `totalMinutes: 32`. |
| Remove Alike | `DELETE /api/screening-programmes/{programmeCode}/items/FILM-002` | Remove Alike and retrieve the programme again. | The delete succeeded; the following GET contained only FILM-001 with count 2 and `totalMinutes: 24`. |
| Submit an invalid count | `PUT /api/screening-programmes/{programmeCode}/items/FILM-001` | Send `{"screeningCount":0}`. Expected: a 4xx validation response and no saved-data change. | The API returned HTTP 400 with `error_code: INVALID_REQUEST` and the message `screening_count must be between 1 and 3`. |
| Verify the saved programme after rejection | `GET /api/screening-programmes/{programmeCode}` | Confirm the invalid update did not change the saved programme. | The GET returned HTTP 200; FILM-001 remained at count 2 and `totalMinutes` remained 24. |

The programme code visible in the validation evidence is `PRG-732f97ef27b3476d9ef20e41b5bdc03a`. The browser screenshots include the corresponding programme responses for the add, update and remove cases.

- [Test 1 — GET response after adding both films](<screenshots/test-01-add-two-films-get-response 6.17.18 AM.png>)
- [Test 2 — API response after updating the screening count](<screenshots/test-02-update-count-api-response 6.18.03 AM.png>)
- [Test 3 — GET response after removing Alike](<screenshots/test-03-remove-alike-get-response 6.20.01 AM.png>)
- [Test 4 — rejected backend update and verification GET](<screenshots/test-04-backend-validation-and-verification 6.29.03 AM.png>)

## Browser or Network Evidence

The browser UI was checked after each operation. The browser Network panel was open for the successful add, update and remove cases, and the screenshots show the corresponding programme state and server response.

1. After adding the two films, the page showed Next Floor and Alike with one screening each and a total of 20 minutes. [Browser and Network screenshot](<screenshots/test-01-add-two-films-ui 6.17.03 AM.png>).
2. After changing Next Floor to two screenings, the page showed Next Floor × 2, Alike × 1 and a total of 32 minutes. [Browser and Network screenshot](<screenshots/test-02-update-count-ui 6.17.53 AM.png>).
3. After removing Alike, the page showed only Next Floor × 2 and a total of 24 minutes. [Browser and Network screenshot](<screenshots/test-03-remove-alike-ui 6.19.49 AM.png>).
4. When zero was entered in the screening-count field, the frontend displayed a red validation message and kept the programme total at 24 minutes. [Frontend validation screenshot](<screenshots/test-04-frontend-validation 6.23.08 AM.png>).

## Log or Console Evidence

The browser Developer Tools Console was used to check the invalid backend request independently of the frontend's client-side validation. A direct PUT request was sent to the programme item endpoint with `{"screeningCount":0}` and the same session headers used for the programme.

The console showed `Invalid PUT status: 400`. The response contained `error_code: INVALID_REQUEST` and `message: screening_count must be between 1 and 3.` The subsequent verification request showed `Verification GET status: 200` and returned a programme with one item, FILM-001 at `screeningCount: 2`, and `totalMinutes: 24`. The captured screenshot shows the request, response, frontend error message and verification result together: [Console validation and verification evidence](<screenshots/test-04-backend-validation-and-verification 6.29.03 AM.png>).

No separate Docker backend log file is included in this evidence set; the console output and API response shown above are the captured diagnostic evidence for this test.

## Issue Found

During the initial frontend integration review, the starter frontend was still wired to the generic catalogue and collection workflow rather than the S02 film and screening-programme API. Its endpoint usage did not match the S02 interface required by the scenario. As a result, the starter page did not yet provide the required film browsing and screening-programme add, update and remove workflow.

The required behaviour was to use the `/films` and `/films/{filmCode}` endpoints for the catalogue and details, and the `/screening-programmes` endpoints for the session programme and its entries. The initial starter workflow did not implement that scenario-specific sequence.

## Fix Applied

The frontend script was updated to implement the S02 workflow. It now loads the film catalogue from `GET /films`, retrieves selected film details from `GET /films/{filmCode}`, creates or retrieves the session programme through `POST /screening-programmes`, and performs programme item additions, updates and removals through the corresponding API endpoints.

Programme requests use the session header through the shared request helper. Programme mutations are queued, and the frontend retrieves the saved programme after a mutation so that the displayed entries and total come from the backend response. The UI also validates screening counts as whole numbers from 1 to 3 and displays an error message when the value is invalid.

## Retest Evidence

After the frontend changes, the four S02 evidence cases were run again against the local application using the same mock session:

- **Add case:** FILM-001 (12 minutes) × 1 plus FILM-002 (8 minutes) × 1 produced 20 minutes in both the browser and programme GET response. The [browser screenshot](<screenshots/test-01-add-two-films-ui 6.17.03 AM.png>) and [API response screenshot](<screenshots/test-01-add-two-films-get-response 6.17.18 AM.png>) record the result.
- **Update case:** Changing FILM-001 to two screenings produced 32 minutes (12 × 2 + 8 × 1). The [browser screenshot](<screenshots/test-02-update-count-ui 6.17.53 AM.png>) and [API response screenshot](<screenshots/test-02-update-count-api-response 6.18.03 AM.png>) record the result.
- **Remove case:** Removing FILM-002 left FILM-001 at two screenings and produced 24 minutes (12 × 2). The [browser screenshot](<screenshots/test-03-remove-alike-ui 6.19.49 AM.png>) and [API response screenshot](<screenshots/test-03-remove-alike-get-response 6.20.01 AM.png>) record the result.
- **Invalid-count case:** The frontend rejected zero with a visible validation message. The direct backend PUT also returned HTTP 400, and a subsequent GET confirmed that the saved count remained 2 and the total remained 24 minutes. The [frontend validation screenshot](<screenshots/test-04-frontend-validation 6.23.08 AM.png>) and [backend validation and verification screenshot](<screenshots/test-04-backend-validation-and-verification 6.29.03 AM.png>) record the result.

The retest results match the S02 expected totals and confirm that the rejected invalid update did not alter the saved programme.
