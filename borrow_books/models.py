from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from transactions.models import Transaction
from books.models import Book
from transactions.constants import RETURN_BOOK

class BorrowHistory(models.Model):
      user = models.ForeignKey(User, related_name='borrow', on_delete=models.CASCADE)
      book = models.ForeignKey(Book, related_name='borrow', on_delete=models.CASCADE)
      borrow_date = models.DateTimeField(auto_now_add=True)
      return_date = models.DateTimeField(blank=True, null=True)
      is_returned = models.BooleanField(default=False)

      class Meta:
            ordering = ['borrow_date']
      