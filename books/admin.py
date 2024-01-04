from django.contrib import admin
from .models import Book, Category, UserBookReview

# Register your models here.
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(UserBookReview)