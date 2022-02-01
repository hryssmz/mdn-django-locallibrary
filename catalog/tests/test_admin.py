# catalog/tests/test_admin.py
from django.contrib.admin.sites import AdminSite
from django.db.transaction import atomic
from django.test import TestCase

from ..admin import BookAdmin
from ..models import Author, Book, Genre


class BookAdminTestCase(TestCase):
    def test_book_admin(self) -> None:
        with atomic():
            Author.objects.create(id=1, first_name="John", last_name="Doe")
            Book.objects.create(
                id=1,
                title="Some Title",
                author_id=1,
                summary="A short summary.",
                isbn="1234567890000",
            )
            Genre.objects.create(id=1, name="Fantasy")
            Genre.objects.create(id=2, name="History")
            Genre.objects.create(id=3, name="Essay")
            Genre.objects.create(id=4, name="Mystery")
            Book.objects.get(id=1).genre.set([1, 2, 3, 4])
        book = Book.objects.get(id=1)
        admin = BookAdmin(model=Book, admin_site=AdminSite())

        self.assertEqual(admin.display_genre(book), "Fantasy, History, Essay")
