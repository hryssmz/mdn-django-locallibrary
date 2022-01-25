# catalog/tests/test_models.py
from django.db.transaction import atomic
from django.test import TestCase

from ..models import Author, Book, BookInstance, Genre


class AuthorTestCase(TestCase):
    def test_create_author(self) -> None:
        author: Author = Author.objects.create(
            id=1,
            first_name="John",
            last_name="Doe",
            date_of_birth="1970-01-01",
        )
        author.refresh_from_db()

        self.assertEqual(author.name, "John, Doe")
        self.assertEqual(author.lifespan, "Jan 01, 1970 - ")
        self.assertEqual(author.url, "/catalog/author/1")
        self.assertEqual(str(author), "John, Doe")


class BookTestCase(TestCase):
    def test_create_book(self) -> None:
        Author.objects.create(id=1, first_name="John", last_name="Doe")

        book: Book = Book.objects.create(
            id=1,
            title="Some Title",
            author_id=1,
            summary="A short summary.",
            isbn="1234567890000",
        )

        self.assertEqual(book.url, "/catalog/book/1")
        self.assertEqual(str(book), "Some Title")


class BookInstanceTestCase(TestCase):
    def test_create_bookinstance(self) -> None:
        with atomic():
            Author.objects.create(id=1, first_name="John", last_name="Doe")
            Book.objects.create(
                id=1,
                title="Some Title",
                author_id=1,
                summary="A short summary.",
                isbn="1234567890000",
            )

        bookinstance: BookInstance = BookInstance.objects.create(
            id="00000000-0000-0000-0000-000000000001",
            book_id=1,
            imprint="Foo Imprint",
            due_back="2020-01-01",
            status="o",
        )
        bookinstance.refresh_from_db()

        self.assertEqual(
            bookinstance.url,
            "/catalog/bookinstance/00000000-0000-0000-0000-000000000001",
        )
        self.assertEqual(bookinstance.due_back_display, "Jan 01, 2020")
        self.assertEqual(
            str(bookinstance),
            "00000000-0000-0000-0000-000000000001 (Some Title)",
        )


class GenreTestCase(TestCase):
    def test_create_genre(self) -> None:
        genre: Genre = Genre.objects.create(id=1, name="Fantasy")

        self.assertEqual(str(genre), "Fantasy")
        self.assertEqual(genre.url, "/catalog/genre/1")
