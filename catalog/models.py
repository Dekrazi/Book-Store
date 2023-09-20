from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django.contrib.auth.models import Permission


class Genre(models.Model):
    name = models.CharField(max_length=100, help_text="Enter a book genre (e.g. Fantasy)")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genre-details", args=[str(self.pk)])


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        ordering = ("last_name", "first_name")

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    title = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.BooleanField(default=True)
    coverpage = models.FileField(upload_to="media/coverpage/")
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])
