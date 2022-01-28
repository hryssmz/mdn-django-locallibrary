# catalog/apis.py
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Author, Book, BookInstance, Genre
from .serializers import (
    AuthorSerializer,
    BookInstanceSerializer,
    BookSerializer,
    GenreSerializer,
)


@api_view()
def index_api(request: Request) -> Response:
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    data = {
        "num_books": Book.objects.all().count(),
        "num_instances": BookInstance.objects.all().count(),
        "num_instances_available": BookInstance.objects.filter(
            status="a"
        ).count(),
        "num_authors": Author.objects.all().count(),
        "num_genres": Genre.objects.all().count(),
        "num_visits": num_visits,
    }
    return Response(data)


class AuthorListAPIView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailAPIView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookInstanceListAPIView(generics.ListAPIView):
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer


class BookInstanceDetailAPIView(generics.RetrieveAPIView):
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetailAPIView(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
