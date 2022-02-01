# catalog/models.py
from datetime import date
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from .utils import format_date


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
        return (
            f"{format_date(self.date_of_birth)} - "
            f"{format_date(self.date_of_death)}"
        )

    @property
    def url(self) -> str:
        return reverse("catalog:author", kwargs={"pk": self.id})

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["id"]


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    summary = models.TextField(max_length=1000)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.ManyToManyField("Genre")

    @property
    def url(self) -> str:
        return reverse("catalog:book", kwargs={"pk": self.id})

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["id"]


class BookInstance(models.Model):
    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=1, choices=LOAN_STATUS, blank=True, default="m"
    )
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def url(self) -> str:
        return reverse("catalog:bookinstance", kwargs={"pk": self.id})

    @property
    def due_back_display(self) -> str:
        return format_date(self.due_back)

    @property
    def is_overdue(self) -> bool:
        return self.due_back and date.today() > self.due_back or False

    def __str__(self) -> str:
        return f"{self.id} ({self.book.title})"

    class Meta:
        ordering = ["id"]
        permissions = (("can_mark_returned", "Set book as returned"),)


class Genre(models.Model):
    name = models.CharField(max_length=200)

    @property
    def url(self) -> str:
        return reverse("catalog:genre", kwargs={"pk": self.id})

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["id"]
