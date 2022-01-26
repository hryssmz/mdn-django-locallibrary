#!/usr/bin/env python
from typing import Optional


def main() -> None:
    from catalog.models import Author, Book, BookInstance, Genre

    def run() -> None:
        authors = init_authors()
        print(f"Initialized {len(authors)} authors!")
        genres = init_genres()
        print(f"Initialized {len(genres)} genres!")
        books = init_books(authors, genres)
        print(f"Initialized {len(books)} books!")
        book_instances = init_book_instances(books)
        print(f"Initialized {len(book_instances)} book instances!")

    def init_book_instances(books: list[Book]) -> list[BookInstance]:
        DATA: list[tuple[Book, str, Optional[str], Optional[str]]] = [
            (books[0], "London Gollancz, 2014.", "a", None),
            (books[1], " Gollancz, 2011.", "o", "2022-12-31"),
            (books[2], " Gollancz, 2015.", None, None),
            (
                books[3],
                "New York Tom Doherty Associates, 2016.",
                "a",
                None,
            ),
            (
                books[3],
                "New York Tom Doherty Associates, 2016.",
                "a",
                None,
            ),
            (
                books[3],
                "New York Tom Doherty Associates, 2016.",
                "a",
                None,
            ),
            (
                books[4],
                "New York, NY Tom Doherty Associates, LLC, 2015.",
                "a",
                None,
            ),
            (
                books[4],
                "New York, NY Tom Doherty Associates, LLC, 2015.",
                "m",
                None,
            ),
            (
                books[4],
                "New York, NY Tom Doherty Associates, LLC, 2015.",
                "o",
                "2022-01-01",
            ),
            (books[0], "Imprint XXX2", None, None),
            (books[1], "Imprint XXX3", None, None),
        ]

        BookInstance.objects.all().delete()
        return BookInstance.objects.bulk_create(
            [
                BookInstance(
                    book=row[0],
                    imprint=row[1],
                    status=row[2] or "m",
                    due_back=row[3],
                )
                for row in DATA
            ]
        )

    def init_books(authors: list[Author], genres: list[Genre]) -> list[Book]:
        DATA: list[tuple[str, Author, str, str, list[Genre]]] = [
            (
                "The Name of the Wind (The Kingkiller Chronicle, #1)",
                authors[0],
                """I have stolen princesses back from sleeping barrow kings. I
burned down the town of Trebon. I have spent the night with Felurian and left
with both my sanity and my life. I was expelled from the University at a younger
age than most people are allowed in. I tread paths by moonlight that others fear
to speak of during day. I have talked to Gods, loved women, and written songs
that make the minstrels weep.""",
                "9781473211896",
                [genres[0]],
            ),
            (
                "The Wise Man's Fear (The Kingkiller Chronicle, #2)",
                authors[0],
                """Picking up the tale of Kvothe Kingkiller once again, we
follow him into exile, into political intrigue, courtship, adventure, love and
magic... and further along the path that has turned Kvothe, the mightiest
magician of his age, a legend in his own time, into Kote, the unassuming pub
landlord.""",
                "9788401352836",
                [genres[0]],
            ),
            (
                "The Slow Regard of Silent Things (Kingkiller Chronicle)",
                authors[0],
                """Deep below the University, there is a dark place. Few people
know of it: a broken web of ancient passageways and abandoned rooms. A young
woman lives there, tucked among the sprawling tunnels of the Underthing, snug in
the heart of this forgotten place.""",
                "9780756411336",
                [genres[0]],
            ),
            (
                "Apes and Angels",
                authors[1],
                """Humankind headed out to the stars not for conquest, nor
exploration, nor even for curiosity. Humans went to the stars in a desperate
crusade to save intelligent life wherever they found it. A wave of death is
spreading through the Milky Way galaxy, an expanding sphere of lethal gamma
...""",
                "9780765379528",
                [genres[1]],
            ),
            (
                "Death Wave",
                authors[1],
                """In Ben Bova's previous novel New Earth, Jordan Kell led the
first human mission beyond the solar system. They discovered the ruins of an
ancient alien civilization. But one alien AI survived, and it revealed to Jordan
Kell that an explosion in the black hole at the heart of the Milky Way galaxy
has created a wave of deadly radiation, expanding out from the core toward
Earth. Unless the human race acts to save itself, all life on Earth will be
wiped out...""",
                "9780765379504",
                [genres[1]],
            ),
            (
                "Test Book 1",
                authors[4],
                "Summary of test book 1",
                "ISBN111111",
                [genres[0], genres[1]],
            ),
            (
                "Test Book 2",
                authors[4],
                "Summary of test book 2",
                "ISBN222222",
                [],
            ),
        ]

        Book.objects.all().delete()
        books: list[Book] = Book.objects.all().bulk_create(
            [
                Book(
                    title=row[0],
                    author=row[1],
                    summary=row[2].replace("\n", " "),
                    isbn=row[3],
                )
                for row in DATA
            ]
        )
        for i in range(len(books)):
            books[i].genre.set(DATA[i][4])
            books[i].save()

        return books

    def init_authors() -> list[Author]:
        DATA: list[tuple[str, str, Optional[str], Optional[str]]] = [
            ("Patrick", "Rothfuss", "1973-06-06", None),
            ("Ben", "Bova", "1932-11-08", None),
            ("Isaac", "Asimov", "1920-01-02", "1992-04-06"),
            ("Bob", "Billings", None, None),
            ("Jim", "Jones", "1971-12-16", None),
        ]

        Author.objects.all().delete()
        return Author.objects.all().bulk_create(
            [
                Author(
                    first_name=row[0],
                    last_name=row[1],
                    date_of_birth=row[2],
                    date_of_death=row[3],
                )
                for row in DATA
            ]
        )

    def init_genres() -> list[Genre]:
        DATA: list[tuple[str]] = [
            ("Fantasy",),
            ("Science Fiction",),
            ("French Poetry",),
        ]

        Genre.objects.all().delete()
        return Genre.objects.all().bulk_create(
            [Genre(name=row[0]) for row in DATA]
        )

    run()


if __name__ == "__main__":
    import os
    from pathlib import Path
    import sys

    import django

    sys.path.append(str(Path(__file__).parents[1]))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    django.setup()
    main()
