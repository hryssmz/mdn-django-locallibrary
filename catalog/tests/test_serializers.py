# catalog/tests/test_serializers.py
from rest_framework.test import APITestCase

from ..models import Author, Book, BookInstance, Genre
from ..serializers import (
    AuthorSerializer,
    BookInstanceSerializer,
    BookSerializer,
    GenreSerializer,
)


class AuthorSerializerTestCase(APITestCase):
    def test_serialize(self) -> None:
        Author.objects.create(
            id=1,
            first_name="John",
            last_name="Doe",
            date_of_birth="1970-01-01",
        )
        ser = AuthorSerializer(Author.objects.get(id=1))

        self.assertDictEqual(
            dict(ser.data),
            {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1970-01-01",
                "date_of_death": None,
            },
        )

    def test_deserialize(self) -> None:
        data = {"first_name": "Lily", "last_name": "Bush"}
        ser = AuthorSerializer(data=data)
        if ser.is_valid():
            ser.save()

        self.assertEqual(Author.objects.count(), 1)


class BookInstanceSerializerTestCase(APITestCase):
    def setUp(self) -> None:
        Author.objects.create(id=1, first_name="John", last_name="Doe")
        Book.objects.create(
            id=1,
            title="Some Title",
            author_id=1,
            summary="A short summary.",
            isbn="1234567890000",
        )

    def test_serialize(self) -> None:
        BookInstance.objects.create(
            id="00000000-0000-0000-0000-000000000001",
            book_id=1,
            imprint="Foo Imprint",
            due_back="2020-01-01",
            status="o",
        )
        ser = BookInstanceSerializer(BookInstance.objects.get(id=1))

        self.assertDictEqual(
            dict(ser.data),
            {
                "id": "00000000-0000-0000-0000-000000000001",
                "book": 1,
                "imprint": "Foo Imprint",
                "due_back": "2020-01-01",
                "status": "o",
            },
        )

    def test_deserialize(self) -> None:
        data = {"book": 1, "imprint": "Foo Imprint", "status": "a"}
        ser = BookInstanceSerializer(data=data)
        if ser.is_valid():
            ser.save()

        self.assertEqual(BookInstance.objects.count(), 1)


class BookSerializerTestCase(APITestCase):
    def setUp(self) -> None:
        Author.objects.create(id=1, first_name="John", last_name="Doe")
        Genre.objects.create(id=1, name="Fantasy")

    def test_serialize(self) -> None:
        Book.objects.create(
            id=1,
            title="Some Title",
            author_id=1,
            summary="A short summary.",
            isbn="1234567890000",
        )
        Book.objects.get(id=1).genre.add(1)
        ser = BookSerializer(Book.objects.get(id=1))

        self.assertDictEqual(
            dict(ser.data),
            {
                "id": 1,
                "title": "Some Title",
                "author": 1,
                "summary": "A short summary.",
                "isbn": "1234567890000",
                "genre": [1],
            },
        )

    def test_deserialize(self) -> None:
        data = {
            "title": "Some Title",
            "author": 1,
            "summary": "A short summary.",
            "isbn": "1234567890000",
            "genre": [1],
        }
        ser = BookSerializer(data=data)
        if ser.is_valid():
            ser.save()

        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get(id=1).genre.all().count(), 1)


class GenreSerializerTestCase(APITestCase):
    def test_serialize(self) -> None:
        Genre.objects.create(id=1, name="Fantasy")
        ser = GenreSerializer(Genre.objects.get(id=1))

        self.assertDictEqual(dict(ser.data), {"id": 1, "name": "Fantasy"})

    def test_deserialize(self) -> None:
        data = {"name": "Fantasy"}
        ser = GenreSerializer(data=data)
        if ser.is_valid():
            ser.save()

        self.assertEqual(Genre.objects.count(), 1)
