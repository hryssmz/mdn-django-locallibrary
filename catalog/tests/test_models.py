# catalog/tests/test_models.py
from django.test import TestCase

from ..models import Author, Book, BookInstance, Genre


class AuthorTest(TestCase):
    def test_create_author(self) -> None:
        author: Author = Author.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth="1970-01-01",
        )
        author.refresh_from_db()

        self.assertEqual(author.name, "John, Doe")
        self.assertEqual(author.lifespan, "Jan 01, 1970 - ")
        self.assertEqual(author.url, "/catalog/author/1")
        self.assertEqual(str(author), "John, Doe")


class BookTest(TestCase):
    def setUp(self) -> None:
        self.author = Author.objects.create(first_name="John", last_name="Doe")

    def test_create_book(self) -> None:
        book: Book = Book.objects.create(
            title="Some Title",
            author_id=self.author.id,
            summary="A short summary.",
            isbn="1234567890000",
        )

        self.assertEqual(book.url, "/catalog/book/1")
        self.assertEqual(str(book), "Some Title")


class BookInstanceTest(TestCase):
    def setUp(self) -> None:
        self.author = Author.objects.create(first_name="John", last_name="Doe")
        self.book = Book.objects.create(
            title="Some Title",
            author_id=self.author.id,
            summary="A short summary.",
            isbn="1234567890000",
        )

    def test_create_bookinstance(self) -> None:
        bookinstance: BookInstance = BookInstance.objects.create(
            book_id=self.book.id,
            imprint="Foo Imprint",
            due_back="2020-01-01",
            status="o",
        )
        bookinstance.refresh_from_db()

        self.assertEqual(
            bookinstance.url, f"/catalog/bookinstance/{bookinstance.id}"
        )
        self.assertEqual(bookinstance.due_back_display, "Jan 01, 2020")
        self.assertEqual(
            str(bookinstance),
            f"{bookinstance.id} ({bookinstance.book.title})",
        )


class GenreTest(TestCase):
    def test_create_genre(self) -> None:
        genre: Genre = Genre.objects.create(name="Fantasy")

        self.assertEqual(str(genre), "Fantasy")
        self.assertEqual(genre.url, "/catalog/genre/1")
