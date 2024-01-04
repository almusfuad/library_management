from django.shortcuts import render
from django.views.generic import ListView
from books.models import Book, Category

# Create your views here.

class HomeView(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'books'

    def get_queryset(self):
        category_slug = self.request.GET.get('category')
        if category_slug:
            return Book.objects.filter(category__category_slug=category_slug)
        else:
            return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context