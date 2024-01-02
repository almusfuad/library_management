from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .constants import GENDER_TYPE
from .models import UserBankAccount, UserAddress


class UserRegistrationForm(UserCreationForm):
      birth_date = forms.DateField(widget = forms.DateInput(attrs = {'type': 'date'}))
      gender = forms.ChoiceField(choices = GENDER_TYPE)
      street_address = forms.CharField(max_length = 100, required=False)
      city = forms.CharField(max_length = 20)
      postal_code = forms.IntegerField()
      country = forms.CharField(max_length = 20)
      
      
      class Meta:
            model = User
            fields = [
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'birth_date',
                  'gender',
                  'postal_code',
                  'city',
                  'country',
                  'street_address',
                  'password1',
                  'password2',
            ]
            
            
      def save(self, commit = True):
            our_user = super().save(commit = False)
            if commit == True:
                  our_user.save()  # Save data to user model
                        
                  # Taking data from user
                  gender = self.cleaned_data.get('gender')
                  postal_code = self.cleaned_data.get('postal_code')
                  country = self.cleaned_data.get('country')
                  birth_date = self.cleaned_data.get('birth_date')
                  city = self.cleaned_data.get('city')
                  street_address = self.cleaned_data.get('street_address')
                        
                        
                        # creating object for address
                  UserAddress.objects.create(
                        user = our_user,
                        postal_code = postal_code,
                        country = country,
                        city = city,
                        street_address = street_address,
                  )
                        
                  # Creating object for bank account
                  UserBankAccount.objects.create(
                        user = our_user,
                        gender = gender,
                        birth_date = birth_date,
                        account_no = 100000 + our_user.id,
                  )
            return our_user
            
            
      #Adding css from backend
      def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
                  
            for field in self.fields:
                  self.fields[field].widget.attrs.update({
                        'class':(
                              'appearance-none block w-full bg-gray-200 '
                              'text-gray-700 border border-gray-200 rounded '
                              'py-3 px-4 leading-tight focus:outline-none '
                              'focus:bg-white focus:border-gray-500'
                        )
                  })