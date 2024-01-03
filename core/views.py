from django.shortcuts import render
from django.views.generic import ListView
from books.models import Book, Category

# Create your views here.

class HomeView(ListView):
      model = Book
      template_name = 'index.html'
      
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['data'] = {
                  'books': Book.objects.all(),
                  'categories': Category.objects.all(),
            }
            return context