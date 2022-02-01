# catalog/urls.py
from django.urls import path

from . import apis, views

app_name = "catalog"
urlpatterns = [
    # Views
    path("", views.index, name="index"),
    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path("author/<int:pk>/", views.AuthorDetailView.as_view(), name="author"),
    path("books/", views.BookListView.as_view(), name="books"),
    path("book/<int:pk>/", views.BookDetailView.as_view(), name="book"),
    path(
        "bookinstances/",
        views.BookInstanceListView.as_view(),
        name="bookinstances",
    ),
    path(
        "bookinstance/<uuid:pk>/",
        views.BookInstanceDetailView.as_view(),
        name="bookinstance",
    ),
    path("genres/", views.GenreListView.as_view(), name="genres"),
    path("genre/<int:pk>/", views.GenreDetailView.as_view(), name="genre"),
    path(
        "mybooks/",
        views.LoanedBooksByUserListView.as_view(),
        name="my-borrowed",
    ),
    # APIs
    path("api/", apis.index_api, name="index-api"),
    path("api/authors/", apis.AuthorListAPIView.as_view(), name="authors-api"),
    path(
        "api/author/<int:pk>/",
        apis.AuthorDetailAPIView.as_view(),
        name="author-api",
    ),
    path("api/books/", apis.BookListAPIView.as_view(), name="books-api"),
    path(
        "api/book/<int:pk>/", apis.BookDetailAPIView.as_view(), name="book-api"
    ),
    path(
        "api/bookinstances/",
        apis.BookInstanceListAPIView.as_view(),
        name="bookinstances-api",
    ),
    path(
        "api/bookinstances/",
        apis.BookInstanceListAPIView.as_view(),
        name="bookinstances-api",
    ),
    path(
        "api/bookinstance/<uuid:pk>/",
        apis.BookInstanceDetailAPIView.as_view(),
        name="bookinstance-api",
    ),
    path("api/genres/", apis.GenreListAPIView.as_view(), name="genre-api"),
    path(
        "api/genre/<int:pk>/",
        apis.GenreDetailAPIView.as_view(),
        name="genre-api",
    ),
]
