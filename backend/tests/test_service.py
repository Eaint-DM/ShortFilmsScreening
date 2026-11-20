import unittest

from app.application.service import (
    ConflictError,
    NotFoundError,
    StarterService,
    ValidationError,
)


class FakeData:
    def __init__(self):
        self.films = [
            {
                "code": "FILM-001",
                "name": "First Film",
                "duration": 12,
                "genre": "Drama",
                "year": 2008,
                "director": "Director One",
                "description": "First description",
                "film_url": "https://example.test/first",
            },
            {
                "code": "FILM-002",
                "name": "Second Film",
                "duration": 8,
                "genre": "Animation",
                "year": 2015,
                "director": "Director Two",
                "description": "Second description",
                "film_url": "https://example.test/second",
            },
        ]

    def health(self):
        return True

    def catalogue(self):
        return self.films

    def catalogue_item(self, film_code):
        return next(
            (film for film in self.films if film["code"] == film_code),
            None,
        )


class FakeCollections:
    def __init__(self):
        self.programmes = {}
        self.session_programmes = {}

    def create_or_get(self, session_code):
        if session_code not in self.session_programmes:
            programme_code = f"PRG-{len(self.programmes) + 1}"
            self.session_programmes[session_code] = programme_code
            self.programmes[programme_code] = []
        return {"programme_code": self.session_programmes[session_code]}

    def read(self, programme_code, session_code):
        if self.session_programmes.get(session_code) != programme_code:
            return None
        return {
            "programme_code": programme_code,
            "items": [dict(item) for item in self.programmes[programme_code]],
        }

    def add(self, programme_code, session_code, entry):
        if self.session_programmes.get(session_code) != programme_code:
            return False
        items = self.programmes[programme_code]
        if any(item["film_code"] == entry["film_code"] for item in items):
            return False
        items.append(dict(entry))
        return True

    def edit(self, programme_code, session_code, film_code, entry):
        if self.session_programmes.get(session_code) != programme_code:
            return False
        for item in self.programmes[programme_code]:
            if item["film_code"] == film_code:
                item.update(entry)
                return True
        return False

    def remove(self, programme_code, session_code, film_code):
        if self.session_programmes.get(session_code) != programme_code:
            return False
        items = self.programmes[programme_code]
        for item in items:
            if item["film_code"] == film_code:
                items.remove(item)
                return True
        return False


class ScreeningProgrammeServiceTests(unittest.TestCase):
    def setUp(self):
        self.collections = FakeCollections()
        self.service = StarterService(FakeData(), self.collections)
        self.session_code = "test-session"
        self.programme_code = self.service.create_programme(
            self.session_code
        )["programmeCode"]

    def test_create_or_get_returns_same_session_programme(self):
        self.assertEqual(
            self.service.create_programme(self.session_code),
            {"programmeCode": self.programme_code},
        )

    def test_catalogue_uses_scenario_response_field_names(self):
        films = self.service.catalogue()

        self.assertEqual(
            films[0]["filmCode"],
            "FILM-001",
        )
        self.assertEqual(films[0]["title"], "First Film")
        self.assertEqual(films[0]["runtimeMinutes"], 12)

    def test_programme_total_updates_on_add_edit_and_remove(self):
        self.service.add_item(
            self.programme_code, self.session_code, "FILM-001", 1
        )
        result = self.service.add_item(
            self.programme_code, self.session_code, "FILM-002", 1
        )
        self.assertEqual(result["totalMinutes"], 20)

        result = self.service.edit_item(
            self.programme_code, self.session_code, "FILM-001", 2
        )
        self.assertEqual(result["totalMinutes"], 32)
        self.assertEqual(result["items"][0]["screeningCount"], 2)

        result = self.service.remove_item(
            self.programme_code, self.session_code, "FILM-002"
        )
        self.assertEqual(result["totalMinutes"], 24)
        self.assertEqual(
            [item["filmCode"] for item in result["items"]],
            ["FILM-001"],
        )

    def test_invalid_counts_leave_saved_entries_and_total_unchanged(self):
        self.service.add_item(
            self.programme_code, self.session_code, "FILM-001", 2
        )

        for invalid_count in (0, 4, True, 1.5):
            with self.subTest(count=invalid_count):
                with self.assertRaises(ValidationError):
                    self.service.edit_item(
                        self.programme_code,
                        self.session_code,
                        "FILM-001",
                        invalid_count,
                    )

                result = self.service.get_programme(
                    self.programme_code, self.session_code
                )
                self.assertEqual(result["items"][0]["screeningCount"], 2)
                self.assertEqual(result["totalMinutes"], 24)

    def test_duplicate_add_and_foreign_session_are_rejected(self):
        self.service.add_item(
            self.programme_code, self.session_code, "FILM-001", 1
        )
        with self.assertRaises(ConflictError):
            self.service.add_item(
                self.programme_code, self.session_code, "FILM-001", 1
            )
        with self.assertRaises(NotFoundError):
            self.service.get_programme(self.programme_code, "other-session")


if __name__ == "__main__":
    unittest.main()
