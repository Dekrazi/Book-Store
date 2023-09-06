from django.shortcuts import render
from django.db.models import Q
from catalog.models import Book, Author, Genre


def search_results(request):
    query = request.GET.get("q")

    books = Book.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ).distinct()

    authors = Author.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query)
    ).distinct()

    genres = Genre.objects.filter(name__icontains=query).distinct()

    return render(
        request,
        "search_results.html",
        {"books": books, "authors": authors, "genres": genres},
    )
