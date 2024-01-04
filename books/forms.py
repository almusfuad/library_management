from django import forms
from .models import UserBookReview
from .constants import BOOK_BORROWER_EXPERIENCE


class BookReviewForm(forms.ModelForm):
      class Meta:
            model = UserBookReview
            fields = ['user_review', 'review_description']
            
            user_review = forms.ChoiceField(
                  choices = BOOK_BORROWER_EXPERIENCE, 
                  widget= forms.Select(attrs = {'class': 'form-control'})
            )
            
            review_description = forms.CharField(
                  max_length = 150,
                  widget = forms.Textarea(attrs = {
                        'class': 'form-control',
                        'rows': 3,
                  })
            )