# catalog/tests/test_apis.py
from django.db.transaction import atomic
from django.test import TestCase
from django.urls import reverse

from ..models import Author, Book, BookInstance, Genre


class IndexApiTestCase(TestCase):
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
            Book.objects.get(id=1).genre.add(Genre.objects.get(id=1))
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

        res = self.client.get(reverse("index-api"))

        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(
            res.json(),
            {
                "num_books": 1,
                "num_instances": 2,
                "num_instances_available": 1,
                "num_authors": 1,
                "num_genres": 1,
            },
        )
