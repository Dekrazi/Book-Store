from django.contrib import admin
from .models import Author, Book, Genre
# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Genre)

class CustomPermissionAdmin(admin.ModelAdmin):
    list_display = ('permission', 'description')