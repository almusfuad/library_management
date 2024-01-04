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
            
      # def save(self, *args, **kwargs):
      #       if self.is_returned and not self.return_date:
      #             # If 'is_returned' is True and 'return_date' is not set, set 'return_date'
      #             self.return_date = timezone.now()

      #             # Refund the amount to the user's account
      #             self.user.account.balance += self.book.borrow_price
      #             self.user.account.save()

      #             # Create a transaction report for the refund
      #             Transaction.objects.create(
      #             account=self.user.account,
      #             amount=self.book.borrow_price,
      #             balance_after_transaction=self.user.account.balance,
      #             transaction_type=RETURN_BOOK
      #             )

      #       super().save(*args, **kwargs)  # Call the original save method
      