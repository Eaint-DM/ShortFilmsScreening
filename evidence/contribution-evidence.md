# Contribution Evidence

Template only: no student implementation or completed evidence is supplied. Replace every TODO with actual observations. Include only assets you reference, using local relative links.

## Contribution Summary

TODO: Record your actual work, date, reproducible steps, expected and observed results, and relevant supporting evidence.

## Individual Contributions

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

TODO: Record your actual work, date, reproducible steps, expected and observed results, and relevant supporting evidence.

## Academic Integrity and Source Acknowledgement

TODO: Identify sources, examples and libraries. Record required AI use: tool, purpose, outputs incorporated, modifications and how each output was verified. Provide honest dated records; do not fabricate evidence.
