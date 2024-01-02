from django.db import models
from django.contrib.auth.models import User
from .constants import BOOK_BORROWER_EXPERIENCE
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
      category_name = models.CharField(max_length = 50)
      
      def __str__(self):
            return self.category_name
      
def book_image_upload(instance, filename):
      return f'books/media/uploads/{instance.book_title}_{filename}'
      
class Book(models.Model):
      book_title = models.CharField(max_length = 50)
      book_description = models.TextField()
      category = models.ManyToManyField(Category, related_name = 'books')
      book_image = models.ImageField(upload_to = book_image_upload, null = True, blank = True)
      borrow_price = models.DecimalField(max_digits = 6, decimal_places=2)
      slug = models.SlugField(unique=True, blank=True, null=True)
      
      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = slugify(f"{self.book_title}")
            return super().save(*args, **kwargs)
      
      def __str__(self):
            return self.book_title
      

class UserBookReview(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
      user_review = models.CharField(max_length=5, choices=BOOK_BORROWER_EXPERIENCE)
      review_description = models.TextField()
      
      def __str__(self):
            return f'{self.user.username}\'s reviewed {self.book.book_title}'
      
      class Meta:
            unique_together = ('user', 'book')
            
      @property
      def numeric_review(self):
            return int(self.user_review)
      
      @classmethod
      def calculate_average_review(cls, book):
            reviews = cls.objects.filter(book=book)
            if reviews.exists():
                  total_reviews = len(reviews)
                  total_score = sum(review.numeric_review for review in reviews)
                  average_score = total_score / total_reviews
                  return round(average_score, 2)
            else:
                  return 0
      
      
      