from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE


# Create your models here.

class UserBankAccount(models.Model):
      user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'bank_account')
      account_no = models.IntegerField(unique = True)
      birth_date = models.DateField(null = True, blank = True)
      gender = models.CharField(max_length = 10, choices = GENDER_TYPE)
      initial_deposit_date = models.DateField(auto_now_add = True)
      balance = models.DecimalField(default = 0, max_digits = 12, decimal_places = 2)
      
      def __str__(self):
            return f'{self.account_no}'
      
      
class UserAddress(models.Model):
      user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'address')
      street_address = models.CharField(max_length = 100, null = True, blank = True)
      city = models.CharField(max_length = 20)
      postal_code = models.IntegerField()
      country = models.CharField(max_length = 10)
      
      def __str__(self):
            return f'{self.user.email}'