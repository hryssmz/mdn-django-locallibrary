# catalog/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Author, Book, BookInstance, Genre


def index(request: HttpRequest) -> HttpResponse:
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_books": Book.objects.all().count(),
        "num_instances": BookInstance.objects.all().count(),
        "num_instances_available": BookInstance.objects.filter(
            status="a"
        ).count(),
        "num_authors": Author.objects.all().count(),
        "num_genres": Genre.objects.all().count(),
        "num_visits": num_visits,
    }
    return render(request, "catalog/index.html", context=context)


class AuthorListView(generic.ListView[Author]):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView[Author]):
    model = Author


class BookListView(generic.ListView[Book]):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView[Book]):
    model = Book


class BookInstanceListView(generic.ListView[BookInstance]):
    model = BookInstance
    paginate_by = 10


class BookInstanceDetailView(generic.DetailView[BookInstance]):
    model = BookInstance


class GenreListView(generic.ListView[Genre]):
    model = Genre
    paginate_by = 10


class GenreDetailView(generic.DetailView[Genre]):
    model = Genre


class LoanedBooksByUserListView(
    LoginRequiredMixin, generic.ListView[BookInstance]
):
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginated_by = 10

    def get_queryset(self) -> QuerySet[BookInstance]:
        return BookInstance.objects.filter(  # type: ignore
            borrower=self.request.user
        )
