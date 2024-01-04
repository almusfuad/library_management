from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView

# authorizations import
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from books.forms import BookReviewForm

# all db models
from .models import BorrowHistory
from transactions.models import Transaction
from transactions.constants import BORROW_BOOK
from books.models import Book, UserBookReview


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


@method_decorator(login_required, name = 'dispatch')
class BorrowHistoryListView(ListView):
      model = BorrowHistory
      template_name = 'borrow_books/borrow_history.html'
      context_object_name = 'borrow_history'
      paginate_by = 10  # numbers of items in a page
      
      def get_queryset(self):
            return BorrowHistory.objects.filter(user = self.request.user).order_by('-borrow_date')
      

# def submit_review(request, book_id):
#       book = get_object_or_404(Book, id = book_id)
#       user = request.user
      
#       # check the user has already reviewed the book or not
#       existing_review = UserBookReview.objects.filter(user = user, book = book)
#       if existing_review.exists():
#             messages.error(request, "Book already reviewed!")
#             return HttpResponseRedirect(redirect('borrow_history'))
      
#       if request.method == 'POST':
#             form = BookReviewForm(request.POST)
#             if form.is_valid():
#                   # save new review
#                   new_review = form.save(commit = False)
#                   new_review.user = user
#                   new_review.book = book
#                   new_review.save()
                  
#                   # update average_reviews in the model
#                   book.average_reviews = UserBookReview.calculate_average_review(book)
#                   book.save()
                  
#                   messages.success(request, 'Review submitted successfully!')
#                   return HttpResponseRedirect(reverse('borrow_history'))
#       else:
#             form = BookReviewForm()
      
#       return render(request, 'borrow_books/submit_review.html', {'form': form, 'book': book})