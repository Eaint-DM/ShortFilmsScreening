import { request } from './http.js';
import { createActionQueue } from './action-queue.js';



// 1. APPLICATION STATE

// One temporary session for this browser page.
const sessionCode = crypto.randomUUID();

// Stores the programme code returned by the backend.
let programmeCode = null;

// Prevents programme operations before initialization.
let programmeReady = false;

// Keeps programme operations in the correct order.
const enqueue = createActionQueue();



// 2. GET HTML ELEMENTS


const filmList = document.querySelector('#film-list');
const filmDetails = document.querySelector('#film-details-content');
const filmCount = document.querySelector('#film-count');
const programmeList = document.querySelector('#programme-list');
const programmeTotal = document.querySelector('#programme-total');
const appMessage = document.querySelector('#app-message');

const sessionDisplay = document.querySelector('#session');
const statusDisplay = document.querySelector('#status');
const outputDisplay = document.querySelector('#output');

// Display the current mock session.
sessionDisplay.textContent = `Mock session: ${sessionCode}`;

function getProgrammePath() {
    return `/screening-programmes/${encodeURIComponent(programmeCode)}`;
}



// 3. DISPLAY APPLICATION MESSAGES


function showMessage(message, type = 'info') {

    appMessage.textContent = message;
    appMessage.className = `app-message ${type}`;

}



// 4. CREATE HTML ELEMENTS SAFELY


function createElement(tag, className, text) {

    const element = document.createElement(tag);

    if (className) {
        element.className = className;
    }

    if (text !== undefined) {
        element.textContent = text;
    }

    return element;

}



// 5. DISPLAY FILM CATALOGUE


function renderFilms(films) {

    filmList.replaceChildren();

    if (films.length === 0) {

        filmList.appendChild(
            createElement(
                'p',
                'empty-state',
                'No films are currently available.'
            )
        );

        return;
    }

    films.forEach(film => {

        const card = createElement(
            'article',
            'film-card'
        );

        const content = createElement(
            'div',
            'film-card-content'
        );

        const title = createElement(
            'h3',
            '',
            film.title
        );

        const code = createElement(
            'p',
            'film-meta',
            film.filmCode
        );

        const runtime = createElement(
            'p',
            'film-meta',
            `${film.runtimeMinutes} minutes · ${film.genre}`
        );

        const year = createElement(
            'p',
            'film-meta',
            `Released: ${film.year}`
        );


        // View Details Button

        const detailsButton = createElement(
            'button',
            'btn-secondary',
            'View details'
        );

        detailsButton.addEventListener('click', () => {

            loadFilmDetails(film.filmCode);

        });


        // Screening Count Input

        const countLabel = createElement(
            'label',
            'screening-count-label',
            'Screenings'
        );

        const countInput = document.createElement('input');

        countInput.type = 'number';
        countInput.className = 'quantity-input';
        countInput.min = '1';
        countInput.max = '3';
        countInput.step = '1';
        countInput.value = '1';

        countInput.setAttribute(
            'aria-label',
            `Screening count for ${film.title}`
        );

        countLabel.appendChild(countInput);


        // Add to Programme Button

        const addButton = createElement(
            'button',
            'btn-primary add-film-button',
            'Add to programme'
        );

        addButton.disabled = !programmeReady;

        addButton.addEventListener('click', () => {

            const screeningCount = Number(countInput.value);

            addFilm(
                film.filmCode,
                screeningCount,
                addButton
            );

        });


        // Assemble Film Card

        content.append(
            title,
            code,
            runtime,
            year,
            detailsButton,
            countLabel,
            addButton
        );

        card.appendChild(content);

        filmList.appendChild(card);

    });

}



// 6. LOAD FILMS FROM BACKEND


async function loadFilms() {

    try {

        const result = await request('/films');

        const films = result.items;

        // Display the actual number of films returned by the API.
        filmCount.textContent = String(films.length).padStart(2, '0');

        renderFilms(films);

        return films.length;

    } catch (error) {

        filmList.replaceChildren(
            createElement(
                'p',
                'empty-state',
                'Unable to load films. Please try again.'
            )
        );

        throw error;

    }

}



// 7. LOAD SELECTED FILM DETAILS


async function loadFilmDetails(filmCode) {

    // Scroll smoothly to Film Details.

    document.querySelector('#film-details').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });

    filmDetails.textContent = 'Loading film details...';

    try {

        const film = await request(
            `/films/${encodeURIComponent(filmCode)}`
        );

        filmDetails.replaceChildren();


        // Film Title

        const title = createElement(
            'h3',
            '',
            film.title
        );


        // Film Information

        const information = createElement(
            'div',
            'film-detail-info'
        );

        const fields = [
            ['Film Code', film.filmCode],
            ['Runtime', `${film.runtimeMinutes} minutes`],
            ['Genre', film.genre],
            ['Release Year', film.year],
            ['Director', film.director]
        ];

        fields.forEach(([label, value]) => {

            const item = createElement(
                'div',
                'film-detail-item'
            );

            item.append(
                createElement('span', '', label),
                createElement('strong', '', value)
            );

            information.appendChild(item);

        });


        // Film Description

        const description = createElement(
            'p',
            '',
            film.description
        );

        filmDetails.append(
            title,
            information,
            description
        );


        // Optional Film Reference Link

        if (film.filmUrl) {

            const filmLink = createElement(
                'a',
                '',
                'Watch film reference'
            );

            filmLink.href = film.filmUrl;
            filmLink.target = '_blank';
            filmLink.rel = 'noopener noreferrer';

            filmDetails.appendChild(filmLink);

        }

        showMessage(
            `Loaded details for ${film.title}.`,
            'success'
        );

    } catch (error) {

        filmDetails.textContent =
            'Unable to load this film information.';

        showMessage(
            `${error.message} ${error.code || ''}`,
            'error'
        );

    }

}



// 8. CREATE OR RETRIEVE PROGRAMME


async function initializeProgramme() {

    try {

        const programme = await enqueue(async () => {

            // Create or retrieve programme for this session.

            const result = await request(
                '/screening-programmes',
                {
                    method: 'POST',
                    session: sessionCode
                }
            );

            programmeCode = result.programmeCode;

            if (!programmeCode) {

                throw new Error(
                    'The backend did not return a programme code.'
                );

            }

            // Retrieve saved programme.

            return await request(
                getProgrammePath(),
                {
                    session: sessionCode
                }
            );

        });


        // Display programme.

        renderProgramme(programme);

        programmeReady = true;


        // Enable Add buttons.

        document.querySelectorAll('.add-film-button')
            .forEach(button => {

                button.disabled = false;

            });

        return true;

    } catch (error) {

        programmeReady = false;

        showMessage(
            `Unable to prepare programme: ${error.message} ${error.code || ''}`,
            'error'
        );

        throw error;

    }

}



// 9. GET LATEST SAVED PROGRAMME


async function refreshProgramme() {

    const programme = await enqueue(async () => {

        return await request(
            getProgrammePath(),
            {
                session: sessionCode
            }
        );

    });

    renderProgramme(programme);

    return programme;

}



// 10. DISPLAY SCREENING PROGRAMME


function renderProgramme(programme) {

    programmeList.replaceChildren();

    const items = programme.items || [];


    // Display the total calculated by the backend.

    programmeTotal.textContent =
        `${programme.totalMinutes ?? 0} minutes`;


    // Empty Programme

    if (items.length === 0) {

        programmeList.appendChild(
            createElement(
                'p',
                'empty-state',
                'Your screening programme is currently empty.'
            )
        );

        return;

    }


    // Create Programme Table

    const table = createElement(
        'table',
        'programme-table'
    );

    const thead = document.createElement('thead');

    const headerRow = document.createElement('tr');

    [
        'Film',
        'Runtime',
        'Screenings',
        'Actions'
    ].forEach(label => {

        headerRow.appendChild(
            createElement('th', '', label)
        );

    });

    thead.appendChild(headerRow);


    // Programme Entries

    const tbody = document.createElement('tbody');

    items.forEach(item => {

        const row = document.createElement('tr');


        // Film Information

        const filmCell = document.createElement('td');

        const filmName = createElement(
            'strong',
            '',
            item.title
        );

        const filmCode = createElement(
            'p',
            'film-meta',
            item.filmCode
        );

        filmCell.append(
            filmName,
            filmCode
        );


        // Runtime

        const runtimeCell = createElement(
            'td',
            '',
            `${item.runtimeMinutes} min`
        );


        // Screening Count Input

        const countCell = document.createElement('td');

        const countInput = document.createElement('input');

        countInput.type = 'number';
        countInput.className = 'quantity-input';
        countInput.min = '1';
        countInput.max = '3';
        countInput.step = '1';
        countInput.value = item.screeningCount;

        countInput.setAttribute(
            'aria-label',
            `Screening count for ${item.title}`
        );

        countCell.appendChild(countInput);


        // Action Buttons

        const actionsCell = document.createElement('td');

        const controls = createElement(
            'div',
            'programme-controls'
        );


        // Update Button

        const updateButton = createElement(
            'button',
            'btn-secondary',
            'Update'
        );

        updateButton.addEventListener('click', () => {

            updateScreeningCount(
                item.filmCode,
                Number(countInput.value),
                updateButton
            );

        });


        // Remove Button

        const removeButton = createElement(
            'button',
            'btn-danger',
            'Remove'
        );

        removeButton.addEventListener('click', () => {

            removeFilm(
                item.filmCode,
                removeButton
            );

        });


        controls.append(
            updateButton,
            removeButton
        );

        actionsCell.appendChild(controls);


        // Assemble Row

        row.append(
            filmCell,
            runtimeCell,
            countCell,
            actionsCell
        );

        tbody.appendChild(row);

    });

    table.append(
        thead,
        tbody
    );

    programmeList.appendChild(table);

}



// 11. RUN PROGRAMME MUTATION


// Shared helper for Add, Update and Remove.

async function runProgrammeMutation({
    button,
    loadingMessage,
    successMessage,
    errorPrefix,
    operation
}) {

    if (!programmeCode || !programmeReady) {

        showMessage(
            'Your screening programme is not ready yet.',
            'error'
        );

        return false;

    }

    button.disabled = true;

    try {

        const updatedProgramme = await enqueue(async () => {

            showMessage(
                loadingMessage,
                'info'
            );

            // Perform the API operation.

            await operation();

            // Retrieve the latest saved programme.

            return await request(
                getProgrammePath(),
                {
                    session: sessionCode
                }
            );

        });


        // Render actual backend data.

        renderProgramme(updatedProgramme);

        showMessage(
            successMessage,
            'success'
        );

        return true;

    } catch (error) {

        // Try to restore the latest saved programme
        // if the operation or refresh failed.

        try {

            await refreshProgramme();

        } catch (refreshError) {

            console.error(
                'Could not refresh programme:',
                refreshError
            );

        }

        showMessage(
            `${errorPrefix}: ${error.message} ${error.code || ''}`,
            'error'
        );

        return false;

    } finally {

        button.disabled = false;

    }

}



// 12. ADD FILM TO PROGRAMME


async function addFilm(
    filmCode,
    screeningCount,
    button
) {

    // Validate screening count before sending request.

    if (
        !Number.isInteger(screeningCount) ||
        screeningCount < 1 ||
        screeningCount > 3
    ) {

        showMessage(
            'Screening count must be a whole number from 1 to 3.',
            'error'
        );

        return;

    }


    const success = await runProgrammeMutation({

        button,

        loadingMessage: 'Adding film to your programme...',

        successMessage: 'Film added to your screening programme.',

        errorPrefix: 'Unable to add film',

        operation: async () => {

            await request(
                `${getProgrammePath()}/items`,
                {
                    method: 'POST',
                    session: sessionCode,
                    body: {
                        filmCode,
                        screeningCount
                    }
                }
            );

        }

    });


    // Scroll to programme after successful addition.

    if (success) {

        document.querySelector('#screening-programme')
            .scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });

    }

}



// 13. UPDATE SCREENING COUNT


async function updateScreeningCount(
    filmCode,
    screeningCount,
    button
) {

    // Only whole numbers from 1 to 3 are allowed.

    if (
        !Number.isInteger(screeningCount) ||
        screeningCount < 1 ||
        screeningCount > 3
    ) {

        showMessage(
            'Screening count must be a whole number from 1 to 3.',
            'error'
        );

        return;

    }


    await runProgrammeMutation({

        button,

        loadingMessage: 'Updating screening count...',

        successMessage: 'Screening count updated successfully.',

        errorPrefix: 'Unable to update screening count',

        operation: async () => {

            await request(
                `${getProgrammePath()}/items/${encodeURIComponent(filmCode)}`,
                {
                    method: 'PUT',
                    session: sessionCode,
                    body: {
                        screeningCount
                    }
                }
            );

        }

    });

}



// 14. REMOVE FILM FROM PROGRAMME


async function removeFilm(filmCode, button) {

    await runProgrammeMutation({

        button,

        loadingMessage: 'Removing film from your programme...',

        successMessage: 'Film removed from your screening programme.',

        errorPrefix: 'Unable to remove film',

        operation: async () => {

            await request(
                `${getProgrammePath()}/items/${encodeURIComponent(filmCode)}`,
                {
                    method: 'DELETE',
                    session: sessionCode
                }
            );

        }

    });

}



// 15. DEVELOPER DIAGNOSTICS


async function runDiagnostic(button, operation) {

    button.disabled = true;

    try {

        const result = await operation();

        outputDisplay.textContent =
            JSON.stringify(result, null, 2);

        statusDisplay.textContent =
            'Request completed successfully.';

    } catch (error) {

        statusDisplay.textContent =
            `${error.message} ${error.code || ''}`;

    } finally {

        button.disabled = false;

    }

}


// Health Check

document.querySelector('#health').addEventListener(
    'click',
    event => {

        runDiagnostic(
            event.currentTarget,
            () => request('/health')
        );

    }
);


// Catalogue Check

document.querySelector('#catalogue').addEventListener(
    'click',
    event => {

        runDiagnostic(
            event.currentTarget,
            () => request('/films')
        );

    }
);


// Disable old generic collection test.

const collectionButton = document.querySelector('#collection');

collectionButton.disabled = true;

collectionButton.textContent =
    'S02 programme controls are now active above';



// 16. START APPLICATION


async function startApplication() {

    showMessage(
        'Loading films and preparing your programme...',
        'info'
    );

    const results = await Promise.allSettled([

        loadFilms(),

        initializeProgramme()

    ]);

    const filmResult = results[0];

    const programmeResult = results[1];


    if (filmResult.status === 'rejected') {

        showMessage(
            `Unable to load films: ${filmResult.reason.message}`,
            'error'
        );

        return;

    }


    if (programmeResult.status === 'rejected') {

        return;

    }


    showMessage(
        `Successfully loaded ${filmResult.value} films. Your programme is ready.`,
        'success'
    );

}


// Start application when page opens.

startApplication();
