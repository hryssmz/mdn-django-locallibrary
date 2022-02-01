# catalog/tests/test_views.py
from django.contrib.auth.models import User
from django.db import transaction
from django.test import TestCase

from ..models import Author, Book, BookInstance, Genre


class IndexTestCase(TestCase):
    def test_get(self) -> None:
        with transaction.atomic():
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
        self.assertEqual(res.context["num_visits"], 0)

    def test_num_visits(self) -> None:
        self.client.get("/catalog/")
        res = self.client.get("/catalog/")

        self.assertEqual(res.context["num_visits"], 1)


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

    def test_pagination(self) -> None:
        Author.objects.bulk_create(
            [
                Author(first_name=f"John{i}", last_name=f"Doe{i}")
                for i in range(11)
            ]
        )
        res = self.client.get("/catalog/authors/")

        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(res.context["paginator"].num_pages, 2)
        self.assertEqual(res.context["paginator"].per_page, 10)


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
    def setUp(self) -> None:
        Author.objects.create(id=1, first_name="John", last_name="Doe")
        Book.objects.create(
            id=1,
            title="Some Title",
            author_id=1,
            summary="A short summary.",
            isbn="1234567890000",
        )

    def test_get(self) -> None:
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

    def test_pagination(self) -> None:
        BookInstance.objects.bulk_create(
            [BookInstance(book_id=1, imprint=f"Imprint{i}") for i in range(11)]
        )
        res = self.client.get("/catalog/bookinstances/")

        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(res.context["paginator"].num_pages, 2)
        self.assertEqual(res.context["paginator"].per_page, 10)


class BookInstanceDetailViewTestCase(TestCase):
    def test_get(self) -> None:
        with transaction.atomic():
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
    def setUp(self) -> None:
        Author.objects.create(id=1, first_name="John", last_name="Doe")

    def test_get(self) -> None:
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

    def test_pagination(self) -> None:
        Book.objects.bulk_create(
            [
                Book(
                    title=f"Title{i}",
                    author_id=1,
                    summary=f"Summary{i}",
                    isbn=f"12345678900{i:02}",
                )
                for i in range(11)
            ]
        )
        res = self.client.get("/catalog/books/")

        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(res.context["paginator"].num_pages, 2)
        self.assertEqual(res.context["paginator"].per_page, 10)


class BookDetailViewTestCase(TestCase):
    def test_get(self) -> None:
        with transaction.atomic():
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

    def test_pagination(self) -> None:
        Genre.objects.bulk_create([Genre(name=f"Genre{i}") for i in range(11)])
        res = self.client.get("/catalog/genres/")

        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(res.context["paginator"].num_pages, 2)
        self.assertEqual(res.context["paginator"].per_page, 10)


class GenreDetailViewTestCase(TestCase):
    def test_get(self) -> None:
        Genre.objects.create(id=1, name="Fantasy")
        res = self.client.get("/catalog/genre/1/")

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "catalog/genre_detail.html")
        self.assertEqual(res.context["genre"].id, 1)


class LoanedBooksByUserListViewTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            username="john", email="john@example.com", password="secret"
        )
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

    def test_get(self) -> None:
        self.client.login(username="john", password="secret")
        res = self.client.get("/catalog/mybooks/")

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            res, "catalog/bookinstance_list_borrowed_user.html"
        )
        self.assertEqual(res.context["bookinstance_list"].count(), 0)

    def test_get_with_borrow(self) -> None:
        BookInstance.objects.filter(id=1).update(
            borrower=User.objects.get(username="john")
        )

        self.client.login(username="john", password="secret")
        res = self.client.get("/catalog/mybooks/")

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            res, "catalog/bookinstance_list_borrowed_user.html"
        )
        self.assertEqual(res.context["bookinstance_list"].count(), 1)
        self.assertEqual(
            str(res.context["bookinstance_list"].first().id),
            "00000000-0000-0000-0000-000000000001",
        )

    def test_get_without_login(self) -> None:
        res = self.client.get("/catalog/mybooks/")

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res, "/accounts/login/?next=%2Fcatalog%2Fmybooks%2F"
        )
