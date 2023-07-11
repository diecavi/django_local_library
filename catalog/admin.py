from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.
# Define the admin class

class BookInLine(admin.TabularInline):
    model = Book
    extra = 1


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    inlines = [BookInLine]



class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 1
    #exclude = ("id",)

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "imprint", "borrower", "due_back", "language", "status")
    list_filter  = ('status', 'due_back')
    fieldsets    = ((None,           {"fields": ("book", "imprint", "language")}),
                    ("Availability", {"fields": ( "borrower", "status", "due_back")}),
                    ("Id",           {"fields": ("id",)}))

admin.site.register(Author, AuthorAdmin)   # Register the admin class with the associated model
admin.site.register(Genre)
admin.site.register(Language)

