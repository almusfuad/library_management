from django.contrib import admin
from .models import BorrowHistory
from django.utils import timezone
from transactions.models import Transaction
from transactions.constants import RETURN_BOOK
from .views import send_borrow_email

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
      
      def save_model(self, request, obj, form, change):
            if obj.is_returned and not obj.return_date:
                  # If 'is_returned' is True and 'return_date' is not set, set 'return_date'
                  obj.return_date = timezone.now()

                  # Refund the amount to the user's account
                  obj.user.account.balance += obj.book.borrow_price
                  obj.user.account.save()

                  # Create a transaction report for the refund
                  Transaction.objects.create(
                  account=obj.user.account,
                  amount=obj.book.borrow_price,
                  balance_after_transaction=obj.user.account.balance,
                  transaction_type=RETURN_BOOK
            )
            send_borrow_email(obj.user, f'Book: {obj.book.book_title}', 'Book Returned', 'borrow_books/emails/return_success.html')
            super().save_model(request, obj, form, change)