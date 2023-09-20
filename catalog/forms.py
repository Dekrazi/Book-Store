from django import forms
from .models import Book, Author, Genre


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"  # Use all fields from the Book model
        widgets = {
            "genre": forms.CheckboxSelectMultiple(),  # Customize genre field widget
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name"]
