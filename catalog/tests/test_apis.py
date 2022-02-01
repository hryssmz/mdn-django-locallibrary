# catalog/tests/test_apis.py
from django.db.transaction import atomic
from rest_framework.test import APITestCase

from ..models import Author, Book, BookInstance, Genre


class IndexApiTestCase(APITestCase):
    def test_get(self) -> None:
        with atomic():
            Author.objects.create(id=1, first_name="John", last_name="Doe")
            Genre.objects.create(id=1, name="Fantasy")
            Book.objects.create(
                title="Some Title",
                author_id=1,
                summary="A short summary.",
                isbn="1234567890000",
            )
            Book.objects.get(id=1).genre.add(1)
            BookInstance.objects.create(
                id="00000000-0000-0000-0000-000000000001",
                book_id=1,
                imprint="Foo Imprint",
                status="m",
            )
            BookInstance.objects.create(
                id="00000000-0000-0000-0000-000000000002",
                book_id=1,
                imprint="Bar Imprint",
                status="a",
            )
        res = self.client.get("/catalog/api/")

        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(
            res.json(),
            {
                "num_books": 1,
                "num_instances": 2,
                "num_instances_available": 1,
                "num_authors": 1,
                "num_genres": 1,
                "num_visits": 0,
            },
        )

    def test_num_visits(self) -> None:
        self.client.get("/catalog/api/")
        res = self.client.get("/catalog/api/")
        data = res.json()

        self.assertEqual(data["num_visits"], 1)


class AuthorListAPIViewTestCase(APITestCase):
    def test_get(self) -> None:
        Author.objects.create(
            id=1,
            first_name="John",
            last_name="Doe",
            date_of_birth="1970-01-01",
        )
        res = self.client.get("/catalog/api/authors/")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)
        self.assertDictEqual(
            res.json()[0],
            {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1970-01-01",
                "date_of_death": None,
            },
        )


class AuthorDetailAPIViewTestCase(APITestCase):
    def test_get(self) -> None:
        Author.objects.create(
            id=1,
            first_name="John",
            last_name="Doe",
            date_of_birth="1970-01-01",
        )
        res = self.client.get("/catalog/api/author/1/")

        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(
            res.json(),
            {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1970-01-01",
                "date_of_death": None,
            },
        )


class BookInstanceListAPIViewTestCase(APITestCase):
    def test_get(self) -> None:
        with atomic():
            Author.objects.create(id=1, first_name="John", last_name="Doe")
            Book.objects.create(
                id=1,
                title="Some Title",
                author_id=1,
                summary="A short summary.",
                isbn="1234567890000",
            )
            BookInstance.objects.create(
                id="00000000-0000-0000-0000-000000000001",
                book_id=1,
                imprint="Foo Imprint",
                due_back="2020-01-01",
                status="o",
            )
        res = self.client.get("/catalog/api/bookinstances/")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)
        self.assertDictEqual(
            res.json()[0],
            {
                "id": "00000000-0000-0000-0000-000000000001",
                "book": 1,
                "imprint": "Foo Imprint",
                "due_back": "2020-01-01",
                "status": "o",
            },
        )


class BookInstanceDetailAPIViewTestCase(APITestCase):
    def test_get(self) -> None:
        with atomic():
            Author.objects.create(id=1, first_name="John", last_name="Doe")
            Book.objects.create(
                id=1,
                title="Some Title",
                author_id=1,
                summary="A short summary.",
                isbn="1234567890000",
            )
            BookInstance.objects.create(
                id="00000000-0000-0000-0000-000000000001",
                book_id=1,
                imprint="Foo Imprint",
                due_back="2020-01-01",
                status="o",
            )
        res = self.client.get(
            "/catalog/api/bookinstance/00000000-0000-0000-0000-000000000001/"
        )

        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(
            res.json(),
            {
                "id": "00000000-0000-0000-0000-000000000001",
                "book": 1,
                "imprint": "Foo Imprint",
                "due_back": "2020-01-01",
                "status": "o",
            },
        )


class BookListAPIViewTestCase(APITestCase):
    def test_get(self) -> None:
        with atomic():
            Author.objects.create(id=1, first_name="John", last_name="Doe")
            Book.objects.create(
                id=1,
                title="Some Title",
                author_id=1,
                summary="A short summary.",
                isbn="1234567890000",
            )
        res = self.client.get("/catalog/api/books/")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)
        self.assertDictEqual(
            res.json()[0],
            {
                "id": 1,
                "title": "Some Title",
                "author": 1,
                "summary": "A short summary.",
                "isbn": "1234567890000",
                "genre": [],
            },
        )


class BookDetailAPIViewTestCase(APITestCase):
    def test_get(self) -> None:
        with atomic():
            Author.objects.create(id=1, first_name="John", last_name="Doe")
            Book.objects.create(
                id=1,
                title="Some Title",
                author_id=1,
                summary="A short summary.",
                isbn="1234567890000",
            )
        res = self.client.get("/catalog/api/book/1/")

        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(
            res.json(),
            {
                "id": 1,
                "title": "Some Title",
                "author": 1,
                "summary": "A short summary.",
                "isbn": "1234567890000",
                "genre": [],
            },
        )


class GenreListAPIViewTestCase(APITestCase):
    def test_get(self) -> None:
        Genre.objects.create(id=1, name="Fantasy")
        res = self.client.get("/catalog/api/genres/")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)
        self.assertDictEqual(res.json()[0], {"id": 1, "name": "Fantasy"})


class GenreDetailAPIViewTestCase(APITestCase):
    def test_get(self) -> None:
        Genre.objects.create(id=1, name="Fantasy")
        res = self.client.get("/catalog/api/genre/1/")

        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(res.json(), {"id": 1, "name": "Fantasy"})
