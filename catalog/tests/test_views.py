# catalog/tests/test_views.py
from django.db.transaction import atomic
from django.test import TestCase

from ..models import Author, Book, BookInstance, Genre


class IndexTestCase(TestCase):
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

        res = self.client.get("/catalog/")

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "catalog/index.html")
        self.assertEqual(res.context["num_books"], 1)
        self.assertEqual(res.context["num_instances"], 2)
        self.assertEqual(res.context["num_instances_available"], 1)
        self.assertEqual(res.context["num_authors"], 1)
        self.assertEqual(res.context["num_genres"], 1)


class AuthorListViewTestCase(TestCase):
    def test_get(self) -> None:
        Author.objects.create(
            id=1,
            first_name="John",
            last_name="Doe",
            date_of_birth="1970-01-01",
        )
        res = self.client.get("/catalog/authors/")

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "catalog/author_list.html")
        self.assertEqual(res.context["author_list"].count(), 1)
        self.assertEqual(res.context["author_list"].first().id, 1)


class AuthorDetailViewTestCase(TestCase):
    def test_get(self) -> None:
        Author.objects.create(
            id=1,
            first_name="John",
            last_name="Doe",
            date_of_birth="1970-01-01",
        )
        res = self.client.get("/catalog/author/1/")

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "catalog/author_detail.html")
        self.assertEqual(res.context["author"].id, 1)


class BookInstanceListViewTestCase(TestCase):
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

        res = self.client.get("/catalog/bookinstances/")

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "catalog/bookinstance_list.html")
        self.assertEqual(res.context["bookinstance_list"].count(), 1)
        self.assertEqual(
            str(res.context["bookinstance_list"].first().id),
            "00000000-0000-0000-0000-000000000001",
        )


class BookInstanceDetailViewTestCase(TestCase):
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
            "/catalog/bookinstance/00000000-0000-0000-0000-000000000001/"
        )

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "catalog/bookinstance_detail.html")
        self.assertEqual(
            str(res.context["bookinstance"].id),
            "00000000-0000-0000-0000-000000000001",
        )


class BookListViewTestCase(TestCase):
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

        res = self.client.get("/catalog/books/")

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "catalog/book_list.html")
        self.assertEqual(res.context["book_list"].count(), 1)
        self.assertEqual(res.context["book_list"].first().id, 1)


class BookDetailViewTestCase(TestCase):
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

        res = self.client.get("/catalog/book/1/")

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "catalog/book_detail.html")
        self.assertEqual(res.context["book"].id, 1)


class GenreListViewTestCase(TestCase):
    def test_get(self) -> None:
        Genre.objects.create(id=1, name="Fantasy")

        res = self.client.get("/catalog/genres/")

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "catalog/genre_list.html")
        self.assertEqual(res.context["genre_list"].count(), 1)
        self.assertEqual(res.context["genre_list"].first().id, 1)


class GenreDetailViewTestCase(TestCase):
    def test_get(self) -> None:
        Genre.objects.create(id=1, name="Fantasy")

        res = self.client.get("/catalog/genre/1/")

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "catalog/genre_detail.html")
        self.assertEqual(res.context["genre"].id, 1)
