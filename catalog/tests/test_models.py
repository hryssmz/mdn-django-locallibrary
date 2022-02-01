# catalog/tests/test_models.py
from datetime import date, timedelta

from django.db import transaction
from django.test import TestCase

from ..models import Author, Book, BookInstance, Genre


class AuthorTestCase(TestCase):
    def test_create_retrieve_author(self) -> None:
        Author.objects.create(
            id=1,
            first_name="John",
            last_name="Doe",
            date_of_birth="1970-01-01",
        )
        author: Author = Author.objects.get(id=1)

        self.assertEqual(author.name, "John, Doe")
        self.assertEqual(author.lifespan, "Jan 01, 1970 - ")
        self.assertEqual(author.url, "/catalog/author/1/")
        self.assertEqual(str(author), "John, Doe")


class BookTestCase(TestCase):
    def test_create_retrieve_book(self) -> None:
        with transaction.atomic():
            Author.objects.create(id=1, first_name="John", last_name="Doe")
            Genre.objects.create(id=1, name="Fantasy")
        Book.objects.create(
            id=1,
            title="Some Title",
            author_id=1,
            summary="A short summary.",
            isbn="1234567890000",
        )
        book: Book = Book.objects.get(id=1)
        book.genre.add(1)

        self.assertEqual(book.genre.count(), 1)
        self.assertEqual(book.url, "/catalog/book/1/")
        self.assertEqual(str(book), "Some Title")


class BookInstanceTestCase(TestCase):
    @transaction.atomic()
    def setUp(self) -> None:
        Author.objects.create(id=1, first_name="John", last_name="Doe")
        Book.objects.create(
            id=1,
            title="Some Title",
            author_id=1,
            summary="A short summary.",
            isbn="1234567890000",
        )

    def test_create_retrieve_bookinstance(self) -> None:
        BookInstance.objects.create(
            id="00000000-0000-0000-0000-000000000001",
            book_id=1,
            imprint="Foo Imprint",
            due_back="2020-01-01",
            status="o",
        )
        bookinstance: BookInstance = BookInstance.objects.get(
            id="00000000-0000-0000-0000-000000000001"
        )

        self.assertEqual(
            bookinstance.url,
            "/catalog/bookinstance/00000000-0000-0000-0000-000000000001/",
        )
        self.assertEqual(bookinstance.due_back_display, "Jan 01, 2020")
        self.assertEqual(
            str(bookinstance),
            "00000000-0000-0000-0000-000000000001 (Some Title)",
        )

    def test_is_overdue(self) -> None:
        BookInstance.objects.create(
            id="00000000-0000-0000-0000-000000000001",
            book_id=1,
            imprint="Foo Imprint",
            status="o",
        )
        bookinstance: BookInstance = BookInstance.objects.get(
            id="00000000-0000-0000-0000-000000000001"
        )

        self.assertFalse(bookinstance.is_overdue)

        bookinstance.due_back = date.today()

        self.assertFalse(bookinstance.is_overdue)

        bookinstance.due_back = date.today() - timedelta(days=1)

        self.assertTrue(bookinstance.is_overdue)


class GenreTestCase(TestCase):
    @transaction.atomic()
    def setUp(self) -> None:
        Author.objects.create(id=1, first_name="John", last_name="Doe")
        Book.objects.create(
            id=1,
            title="Some Title",
            author_id=1,
            summary="A short summary.",
            isbn="1234567890000",
        )

    def test_create_retrieve_genre(self) -> None:
        Genre.objects.create(id=1, name="Fantasy")
        genre = Genre.objects.get(id=1)
        genre.book_set.add(1)

        self.assertEqual(genre.book_set.count(), 1)
        self.assertEqual(str(genre), "Fantasy")
        self.assertEqual(genre.url, "/catalog/genre/1/")
