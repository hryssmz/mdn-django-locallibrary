# catalog/tests/test_apis.py
from django.test import TestCase
from django.urls import reverse

from ..models import Author, Book, BookInstance, Genre


class IndexApiTest(TestCase):
    def setUp(self) -> None:
        author = Author.objects.create(first_name="John", last_name="Doe")
        genre = Genre.objects.create(name="Fantasy")
        book = Book.objects.create(
            title="Some Title",
            author_id=author.id,
            summary="A short summary.",
            isbn="1234567890000",
        )
        book.genre.add(genre)
        BookInstance.objects.create(
            book_id=book.id, imprint="Foo Imprint", status="m"
        )
        BookInstance.objects.create(
            book_id=book.id, imprint="Bar Imprint", status="a"
        )

    def test_get(self) -> None:
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
