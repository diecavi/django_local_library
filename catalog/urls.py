from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("",                views.index,                      name="index"),
    path("books/",          views.BookListView.as_view(),     name="books"),
    path("genres/",         views.GenreListView.as_view(),    name="genres"),
    path("languages/",      views.LanguageListView.as_view(), name="languages"),
    path("book/<int:pk>",   views.BookDetailView.as_view(),   name="book-detail"),
    path("authors/",        views.AuthorListView.as_view(),   name="authors"),
    path("author/<int:pk>", views.AuthorDetailView.as_view(), name="author-detail"),
    #path("book/<int:pk>", views.book_detail, name="book-detail")
]


urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]


urlpatterns += [
    path("book/<uuid:pk>/renew/", views.renew_book_librarian, name="renew-book-librarian"),
]


urlpatterns += [
    path('dbmaint/', views.dbmaint, name='dbmaint'),
]


urlpatterns += [
    path('author/create/',          views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]


urlpatterns += [
    path('book/create/',          views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]

