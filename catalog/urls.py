from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("manage_catalog/", views.manage_catalog, name="manage-catalog"),
    path("books", views.BookListView.as_view(), name="books"),
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book-detail"),
    path("add_book/", views.add_book, name="add-book"),
    path("edit_book/<int:book_id>", views.edit_book, name="edit-book"),
    path("delete_book/<int:book_id>/", views.delete_book, name="delete-book"),
    path("add_author/", views.add_author, name="add-author"),
    path("authors", views.AuthorListView.as_view(), name="authors"),
    path("authors/<int:pk>", views.AuthorDetailView.as_view(), name="author-detail"),
    path("edit_author/<int:author_id>", views.edit_author, name="edit-author"),
    path("delete_author/<int:author_id>/", views.delete_author, name="delete-author"),
    path("genres/", views.genre_list, name="genre-list"),
    path("genre/<int:pk>/", views.GenreDetailView.as_view(), name="genre-details"),
    path("add_genre/", views.add_genre, name="add-genre"),
    path("edit_genre/<int:genre_id>", views.edit_genre, name="edit-genre"),
    path("delete_genre/<int:genre_id>/", views.delete_genre, name="delete-genre"),
]
