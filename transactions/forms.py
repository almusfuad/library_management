from django import forms
from .models import Transaction
from django.core.exceptions import ValidationError
from accounts.models import UserBankAccount


class TransactionForm(forms.ModelForm):
      class Meta:
            model = Transaction
            fields = ['amount', 'transaction_type']
            
            
            def __init__(self, *args, **kwargs):
                  self.account = kwargs.pop('bank_account')
                  super().__init__(*args, **kwargs)
                  self.fields['transaction_type'].disabled = True
                  self.fields['transaction_type'].widget = forms.HiddenInput()
                  
                  
            def save(self, commit = True):
                  self.instance.account = self.account
                  self.instance.balance_after_transaction = self.account.balance 
                  return super().save()
            
class DepositForm(TransactionForm):
      def clean_amount(self):
            min_deposit_amount = 100
            amount = self.cleaned_data.get('amount')
            if amount < min_deposit_amount:
                  raise ValidationError(f"Minimum deposit amount is {min_deposit_amount}")
            return amount
      
      
class WithdrawForm(TransactionForm):
      def clean_amount(self):
            account = self.bank_account
            min_withdraw_amount = 100
            max_withdraw_amount = 2000
            balance = account.balance
            amount = self.cleaned_data.get('amount')
            if amount < min_withdraw_amount:
                  raise forms.ValidationError(f'You can withdraw minimum {min_withdraw_amount}.')
            if amount > max_withdraw_amount:
                  raise forms.ValidationError(f'You can withdraw maximum {max_withdraw_amount}.')
            if amount > balance:
                  raise forms.ValidationError(f'You do not have sufficient balance.')