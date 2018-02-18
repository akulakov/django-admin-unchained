from django.contrib import admin
from .models import Author, Book

class AuthorAdmin(admin.ModelAdmin):
    pass

class BookAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'published')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
