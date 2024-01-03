from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from transactions.models import Transaction

# Create your models here.
class BorrowHistory(models.Model):
      user = models.ForeignKey(User, related_name='borrow', on_delete=models.CASCADE)
      book = models.ForeignKey(Book, related_name = 'borrow', on_delete=models.CASCADE)
      borrow_date = models.DateTimeField(auto_now_add = True)
      return_date = models.DateTimeField(blank=True, null=True)
      
      def mark_as_returned(self):
            self.return_date = timezone.now()
            self.save()
            
      class Meta:
            ordering = ['borrow_date']
      