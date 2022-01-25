# catalog/serializers.py
from rest_framework import serializers

from .models import Author, Book, BookInstance, Genre


class AuthorSerializer(serializers.ModelSerializer[Author]):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer[Book]):
    class Meta:
        model = Book
        fields = "__all__"


class BookInstanceSerializer(serializers.ModelSerializer[BookInstance]):
    class Meta:
        model = BookInstance
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer[Genre]):
    class Meta:
        model = Genre
        fields = "__all__"
