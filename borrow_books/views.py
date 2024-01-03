from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from django.views.generic import ListView

# authorizations import
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# all db models
from .models import BorrowHistory
from transactions.models import Transaction
from transactions.constants import BORROW_BOOK
from books.models import Book


@method_decorator(login_required, name = 'dispatch')
class BorrowBookView(View):
      def get(self, request, *args, **kwargs):
        return redirect('transaction_report')
      
      def post(self, request, *args, **kwargs):
            book_id = self.request.POST.get('book_id')
            book = Book.objects.get(id = book_id)
            user = self.request.user
            
            # check for balance
            if user.account.balance < book.borrow_price:
                  messages.error(self.request, 'You have insufficient balance. Please deposit first.')
                  return redirect('deposit_money')
            
            
            # create borrow_history
            borrow_history = BorrowHistory.objects.create(
                  user = user,
                  book = book,
            )
            
            # create transaction_history
            Transaction.objects.create(
                  account = user.account,
                  amount = book.borrow_price,
                  balance_after_transaction = user.account.balance - book.borrow_price,
                  transaction_type = BORROW_BOOK,
            )
            
            # update user account balance
            user.account.balance -= book.borrow_price
            user.account.save()
            
            messages.success(self.request, f'{borrow_history.book.book_title} has borrowed successfully.')
            return redirect('transaction_report')


class BorrowHistoryListView(ListView):
      model = BorrowHistory
      template_name = 'borrow_books/borrow_history.html'
      context_object_name = 'borrow_history'
      paginate_by = 10  # numbers of items in a page
      
      def get_queryset(self):
            return BorrowHistory.objects.filter(user = self.request.user).order_by('-borrow_date')