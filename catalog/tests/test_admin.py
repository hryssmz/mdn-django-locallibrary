# catalog/tests/test_admin.py
from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from ..admin import BookAdmin
from ..models import Author, Book


class BookAdminTest(TestCase):
    def setUp(self) -> None:
        self.author = Author.objects.create(first_name="John", last_name="Doe")
        self.book = Book.objects.create(
            title="Some Title",
            author_id=self.author.id,
            summary="A short summary.",
            isbn="1234567890000",
        )
        self.book.genre.create(name="Fantasy")
        self.book.genre.create(name="Genre2")
        self.book.genre.create(name="Genre3")
        self.book.genre.create(name="Genre4")

    def test_book_admin(self) -> None:
        book_admin = BookAdmin(model=Book, admin_site=AdminSite())

        self.assertEqual(
            book_admin.display_genre(self.book), "Fantasy, Genre2, Genre3"
        )
