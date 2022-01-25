# catalog/views.py
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Author, Book, BookInstance, Genre


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_books": Book.objects.all().count(),
        "num_instances": BookInstance.objects.all().count(),
        "num_instances_available": BookInstance.objects.filter(
            status="a"
        ).count(),
        "num_authors": Author.objects.all().count(),
        "num_genres": Genre.objects.all().count(),
    }
    return render(request, "index.html", context=context)


class AuthorListView(generic.ListView[Author]):
    model = Author


class AuthorDetailView(generic.DetailView[Author]):
    model = Author


class BookListView(generic.ListView[Book]):
    model = Book


class BookDetailView(generic.DetailView[Book]):
    model = Book
