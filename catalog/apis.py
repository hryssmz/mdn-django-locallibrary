# catalog/apis.py
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Author, Book, BookInstance, Genre


@api_view(["GET"])
def index_api(request: Request) -> Response:
    data = {
        "num_books": Book.objects.all().count(),
        "num_instances": BookInstance.objects.all().count(),
        "num_instances_available": BookInstance.objects.filter(
            status="a"
        ).count(),
        "num_authors": Author.objects.all().count(),
        "num_genres": Genre.objects.all().count(),
    }
    return Response(data)
