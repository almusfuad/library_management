from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import UserBookReview, Book
from .constants import BOOK_BORROWER_EXPERIENCE
from .forms import BookReviewForm
from django.views.generic import DetailView


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


class BookDetailView(DetailView):
      model = Book
      template_name = 'books/book_detail.html'
      context_object_name = 'book_details'
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            
            # Retrieve the book object using the slug parameter
            slug = self.kwargs.get('slug')
            book = get_object_or_404(Book, slug=slug)
            
            # retrieve all reviews
            reviews = UserBookReview.objects.filter(book=book).order_by('-review_date')
            
            # Map user as user input
            review_mapping = dict(BOOK_BORROWER_EXPERIENCE)
            
            # Add reviews to the context
            context['reviews'] = [{
                  'user': review.user,
                  'rating': review_mapping.get(reviews.user_review, 'Unknown'),
                  'description': review.review_description,
            } 
            for review in reviews]
            
            return context
            