from django.shortcuts import render
try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy
from django.contrib import admin

from admin_unchained.admin import AUAdmin
from admin_unchained.views import AUListView, AUAddOrChangeView, AUDeleteView

from .models import Book, Author

def make_published(modeladmin, request, queryset):
    print ('In make_published()', queryset)
make_published.short_description = 'Set books as published'

# class AuthorInline(admin.StackedInline):
    # model = Author
class BookInline(admin.StackedInline):
    model = Book
    extra = 1

class AuthorAdmin(AUAdmin):
    model = Author
    list_display = ('pk', 'last_name')
    list_per_page = 20
    add_url_name = 'book_add'
    # change_url_name = 'book_change'
    raw_id_fields = ()
    inlines = [BookInline]

class BookAdmin(AUAdmin):
    model = Book
    list_display = ('pk', 'title', 'published', 'get_authors')
    search_fields = ('title', 'authors__last_name')
    list_filter = ('published', 'authors')
    actions = (make_published,)
    actions_on_top = True
    list_per_page = 20
    add_url_name = 'book_add'
    change_url_name = 'book_change'
    raw_id_fields = ()
    # inlines = [AuthorInline]

class AuthorListView(AUListView):
    model = Author
    admin_class = AuthorAdmin

class BookListView(AUListView):
    model = Book
    admin_class = BookAdmin

class BookAddOrChangeView(AUAddOrChangeView):
    model = Book
    admin_class = BookAdmin
    success_url = reverse_lazy('books')
    delete_url_name = 'book_delete'

class AuthorAddOrChangeView(AUAddOrChangeView):
    model = Author
    admin_class = AuthorAdmin
    success_url = reverse_lazy('authors')

class BookDeleteView(AUDeleteView):
    model = Book
    admin_class = BookAdmin
    success_url = reverse_lazy('books')
