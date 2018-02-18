from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),

    url(r'^author/(?P<pk>.+)/change/$',
        views.AuthorAddOrChangeView.as_view(),
        name='author_change'),

    url(r'^$', views.BookListView.as_view(), name='books'),

    url(r'^(?P<pk>.+)/change/$',
        views.BookAddOrChangeView.as_view(),
        name='book_change'),

    url(r'^(?P<pk>.+)/delete/$',
        views.BookDeleteView.as_view(),
        name='book_delete'),
    url(r'^add/$',
        views.BookAddOrChangeView.as_view(),
        name='book_add'),
]
