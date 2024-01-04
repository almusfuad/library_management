from django.urls import path
from .views import submit_review, BookDetailView

urlpatterns = [
      path('submit_review/<int:book_id>/', submit_review, name = 'submit_review'),
      path('book/<slug:slug>/', BookDetailView.as_view(), name = 'book_detail'),
]