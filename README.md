
Admin Unchained
===

The goal of this package is to make some of the functionality of `contrib.admin` available
outside of the admin site.

Tested with Django 1.11 and 2.0.2

This package may be useful for:
---

 - Customization that is impossible or too complex in the admin.
 - Making admin listing or change form available to non-staff users.
 - Making an alternative admin listing with different columns or other elements, e.g. a
   simpler more compact listing for some use cases while a full admin listing is still
   available in the admin.
 - Making admin listing available to users who do not have the change permissions for
   the respective model.
 - Custom / explicit permissioning for each view.

The following admin functionality is made available:
---

 - Sorting, filtering, pagination, search and actions.
 - Declaration of columns using the same attribute (`list_display`) as in the admin.
 - Add, change, and delete confirmation forms with the same actions as in the admin.

Limitations:
---

 - The Admin can look up and create related records, since it usually has all of the models
   loaded and managed in the admin site. Admin Unchained package is not meant and would not
   make much sense for this use-case so it currently doesn't support it.

TODO
---
 - Add inlines to change / add views.
 - Add history view.

Quickstart
---

For example, if we have a model `Book` as shown:

    class Book(models.Model):
        authors = models.ManyToManyField(Author)
        title = models.CharField(max_length=150)
        published = models.DateField()
        num_pages = models.IntegerField()
        out_of_print = models.BooleanField(default=False)

In our views, we'll first import the admin and base views:

    from admin_unchained.admin import AUAdmin
    from admin_unchained.views import AUListView, AUAddOrChangeView, AUDeleteView

Then we'll inherit from the `AUAdmin` and set it up:

    class BookAdmin(AUAdmin):
        model = Book
        list_display = ('pk', 'title', 'published')
        search_fields = ('title', 'authors__last_name')
        list_filter = ('published', 'authors')
        actions_on_top = True
        list_per_page = 20
        raw_id_fields = ()

        # add_url_name = 'book_add'
        # change_url_name = 'book_change'
        # actions = (make_published,)

Making an admin-like listing is as simple as inheriting from `AUListView`:

    class BookListView(AUListView):
        model = Book
        admin_class = BookAdmin

You can now add a url for it to your urls:

    url(r'^$', views.BookListView.as_view(), name='books'),

If you need add, change and delete views, you can add them as follows:

    class BookAddOrChangeView(AUAddOrChangeView):
        model = Book
        admin_class = BookAdmin
        success_url = reverse_lazy('books')
        delete_url_name = 'book_delete'

    class BookDeleteView(AUDeleteView):
        model = Book
        admin_class = BookAdmin
        success_url = reverse_lazy('books')

To link them to the listing admin, you can uncomment the commented lines above in the admin
setup, and add the following to your urls file:

    url(r'^(?P<pk>.+)/change/$',
        views.BookAddOrChangeView.as_view(),
        name='book_change'),
    url(r'^(?P<pk>.+)/delete/$',
        views.BookDeleteView.as_view(),
        name='book_delete'),
    url(r'^add/$',
        views.BookAddOrChangeView.as_view(),
        name='book_add'),

Finally, you can uncomment the actions line in the admin setup and add an action function
somewhere before the admin class:

    def make_published(modeladmin, request, queryset):
        print ('In make_published()', queryset)
    make_published.short_description = 'Set books as published'

Example app
---
You can look under `example_app` to see the example admin, views and urls.
