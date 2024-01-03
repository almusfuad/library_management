from django.contrib import admin
from .models import BorrowHistory
from django.utils import timezone
from transactions.models import Transaction
from transactions.constants import RETURN_BOOK

# Register your models here.
@admin.register(BorrowHistory)
class BorrowHistoryAdmin(admin.ModelAdmin):
      list_display = [
            'user',
            'book',
            'borrow_date',
            'return_date',
            'is_returned',
      ]
      
      readonly_fields = ['return_date']
      actions = ['mark_as_returned']
      
      def save(self, *args, **kwargs):
            if self.is_returned and not self.return_date:
                  # If 'is_returned' is True and 'return_date' is not set, set 'return_date'
                  self.return_date = timezone.now()

                  # Refund the amount to the user's account
                  self.user.account.balance += self.book.borrow_price
                  self.user.account.save()

                  # Create a transaction report for the refund
                  Transaction.objects.create(
                  account=self.user.account,
                  amount=self.book.borrow_price,
                  balance_after_transaction=self.user.account.balance,
                  transaction_type=RETURN_BOOK
                  )

            super().save(*args, **kwargs)  # Call the original save method