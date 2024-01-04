from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import UserBookReview, Book
from .forms import BookReviewForm


# Create your views here.
def submit_review(request, book_id):
      book = get_object_or_404(Book, id = book_id)
      user = request.user
      
      # check the user has already reviewed the book or not
      existing_review = UserBookReview.objects.filter(user = user, book = book)
      if existing_review.exists():
            messages.error(request, "Book already reviewed!")
            return HttpResponseRedirect(reverse('borrow_history'))
      
      if request.method == 'POST':
            form = BookReviewForm(request.POST)
            if form.is_valid():
                  # save new review
                  new_review = form.save(commit = False)
                  new_review.user = user
                  new_review.book = book
                  new_review.save()
                  
                  # update average_reviews in the model
                  book.average_reviews = UserBookReview.calculate_average_review(book)
                  book.save()
                  
                  messages.success(request, 'Review submitted successfully!')
                  return HttpResponseRedirect(reverse('borrow_history'))
      else:
            form = BookReviewForm()
      
      return render(request, 'books/submit_review.html', {'form': form, 'book': book})