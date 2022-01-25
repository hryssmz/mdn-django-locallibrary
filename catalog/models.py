# catalog/models.py
import uuid

from django.db import models
from django.urls import reverse


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    @property
    def name(self) -> str:
        return f"{self.first_name}, {self.last_name}"

    @property
    def lifespan(self) -> str:
        return f"{self.date_of_birth or ''} - {self.date_of_death or ''}"

    @property
    def view_url(self) -> str:
        return reverse("author-detail", kwargs={"pk": self.id})

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    summary = models.TextField(max_length=1000)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.ManyToManyField("Genre")

    @property
    def view_url(self) -> str:
        return reverse("book-detail", kwargs={"pk": self.id})

    def __str__(self) -> str:
        return self.title


class BookInstance(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=1, choices=LOAN_STATUS, blank=True, default="m"
    )

    def __str__(self) -> str:
        return f"{self.id} ({self.book.title})"


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
