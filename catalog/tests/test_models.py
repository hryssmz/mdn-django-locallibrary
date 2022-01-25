# catalog/tests/test_models.py
from django.test import TestCase

from ..models import Author, Book, BookInstance, Genre


class AuthorTest(TestCase):
    def test_create_author(self) -> None:
        author: Author = Author.objects.create(
            first_name="John", last_name="Doe", date_of_birth="1970-01-01"
        )

        self.assertEqual(author.name, "John, Doe")
        self.assertEqual(author.lifespan, "1970-01-01 - ")
        self.assertEqual(author.view_url, "/catalog/author/1")
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

        self.assertEqual(book.view_url, "/catalog/book/1")
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

    def test_create_book_instance(self) -> None:
        book_instance: BookInstance = BookInstance.objects.create(
            book_id=self.book.id,
            imprint="Foo Imprint",
            due_back="2020-01-01",
            status="o",
        )

        self.assertEqual(
            str(book_instance),
            f"{book_instance.id} ({book_instance.book.title})",
        )


class GenreTest(TestCase):
    def test_create_genre(self) -> None:
        genre = Genre.objects.create(name="Fantasy")

        self.assertEqual(str(genre), "Fantasy")
