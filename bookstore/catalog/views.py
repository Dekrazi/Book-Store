from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from catalog.models import Book, Author, Genre
from .forms import BookForm, AuthorForm, GenreForm


def index(request):
    return redirect("books")


# BOOK
class BookListView(generic.ListView):
    model = Book
    paginate_by = 14

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Book.objects.filter(
                Q(title__icontains=query)
                | Q(author__first_name__icontains=query)
                | Q(author__last_name__icontains=query)
            )
        return Book.objects.all()


class BookDetailView(generic.DetailView):
    model = Book


def user_in_book_store_staff_group(user):
    return user.groups.filter(name="Book Store Staff").exists()


@user_passes_test(user_in_book_store_staff_group)
def manage_catalog(request):
    books = Book.objects.all()
    authors = Author.objects.all()
    genres = Genre.objects.all()

    return render(
        request,
        "catalog/manage_catalog.html",
        {"books": books, "authors": authors, "genres": genres},
    )


@user_passes_test(user_in_book_store_staff_group)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("books")
    else:
        form = BookForm()

    return render(request, "add_book.html", {"form": form})


@user_passes_test(user_in_book_store_staff_group)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("books")
    else:
        form = BookForm(instance=book)
    return render(request, "edit_book.html", {"form": form, "book": book})


@user_passes_test(user_in_book_store_staff_group)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("books")
    return render(request, "delete_book.html", {"book": book})


@user_passes_test(user_in_book_store_staff_group)
def book_list(request):
    books = Book.objects.all()
    return render(request, "book_list.html", {"books": books})


# AUTHOR
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Author.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
        return Author.objects.all()


class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        context["book_list"] = author.book_set.all()
        return context


@user_passes_test(user_in_book_store_staff_group)
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manage-catalog")
    else:
        form = AuthorForm()

    return render(request, "add_author.html", {"form": form})


@user_passes_test(user_in_book_store_staff_group)
def edit_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect("authors")
    else:
        form = AuthorForm(instance=author)

    return render(request, "edit_author.html", {"form": form, "author": author})


@user_passes_test(user_in_book_store_staff_group)
def delete_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == "POST":
        author.delete()
        return redirect("authors")

    return render(request, "delete_author.html", {"author": author})


# GENRE
class GenreDetailView(generic.DetailView):
    model = Genre
    template_name = "catalog/genre_details.html"
    context_object_name = "selected_genre"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = Book.objects.filter(genre=self.object)
        return context


@user_passes_test(user_in_book_store_staff_group)
def add_genre(request):
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add-genre")
    else:
        form = GenreForm()

    return render(request, "add_genre.html", {"form": form})


@user_passes_test(user_in_book_store_staff_group)
def edit_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    if request.method == "POST":
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return redirect("genre-list")
    else:
        form = GenreForm(instance=genre)

    return render(request, "edit_genre.html", {"form": form, "genre": genre})


@user_passes_test(user_in_book_store_staff_group)
def delete_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    if request.method == "POST":
        genre.delete()
        return redirect("genre-list")

    return render(request, "delete_genre.html", {"genre": genre})


def genre_list(request):
    genres = Genre.objects.all()
    return render(request, "catalog/genre_list.html", {"genres": genres})
