from django.urls import path
from .views import BorrowBookView, BorrowHistoryListView


urlpatterns = [
      path('', BorrowBookView.as_view(), name = 'click_borrow'),
      path('borrow_history/', BorrowHistoryListView.as_view(), name = 'borrow_history'),
      
]