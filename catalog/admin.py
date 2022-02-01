# catalog/admin.py
from django.contrib import admin

from .models import Author, Book, BookInstance, Genre


class BookInstanceInline(admin.TabularInline[BookInstance]):
    model = BookInstance


class BookInline(admin.TabularInline[Book]):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin[Author]):
    list_display = ("last_name", "first_name", "date_of_birth", "date_of_death")
    fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin[Book]):
    list_display = ("title", "author", "display_genre")
    inlines = [BookInstanceInline]

    @admin.display(description="Genre")
    def display_genre(self, book: Book) -> str:
        return ", ".join(genre.name for genre in book.genre.all()[:3])


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin[BookInstance]):
    list_display = ("book", "status", "due_back")
    list_filter = ("status", "due_back")
    fieldsets = (
        (None, {"fields": ("book", "imprint", "id")}),
        ("Availability", {"fields": ("status", "due_back", "borrower")}),
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin[Genre]):
    list_display = ("name",)
