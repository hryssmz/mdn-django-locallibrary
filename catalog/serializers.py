# catalog/serializers.py
from rest_framework import serializers

from .models import Author, Book, BookInstance, Genre


class AuthorSerializer(serializers.ModelSerializer[Author]):
    class Meta:
        model = Author
        fields = [
            "id",
            "first_name",
            "last_name",
            "date_of_birth",
            "date_of_death",
        ]


class BookSerializer(serializers.ModelSerializer[Book]):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "summary", "isbn", "genre"]


class BookInstanceSerializer(serializers.ModelSerializer[BookInstance]):
    class Meta:
        model = BookInstance
        fields = ["id", "book", "imprint", "due_back", "status"]


class GenreSerializer(serializers.ModelSerializer[Genre]):
    class Meta:
        model = Genre
        fields = ["id", "name"]
