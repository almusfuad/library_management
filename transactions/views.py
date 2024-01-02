# Import for compatibility
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages

# import from ClassBasedViewModel
from django.views.generic import CreateView, ListView

# Import for authorizations
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.db.models import Sum

# import from transactions app
from .models import Transaction
from .forms import DepositForm, WithdrawForm
from .constants import DEPOSIT, WITHDRAW, BORROW_BOOK, RETURN_BOOK




# single transactions view for make deposit, withdraw
class TransactionCreateMixin(LoginRequiredMixin, CreateView):
      template_name = 'transactions/transaction_forms.html'
      model = Transaction
      title = ''
      success_url = reverse_lazy('transaction_report')
      
      def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs.update({
                  'account': self.request.user.account
            })
            return kwargs
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context.update({
                  'title': self.title
            })
            return context

class DepositMoneyView(TransactionCreateMixin):
      form_class = DepositForm
      title = 'Deposit Money'
      
      def get_initial(self):
            initial = {'transaction_type': DEPOSIT}
            return initial
      
      def form_valid(self, form):
            amount = form.cleaned_data.get('amount')
            account = self.request.user.account
            account.balance += amount
            account.save(
                  update_fields = ['balance']
            )
            messages.success(self.request, f'BDT {amount} was deposited successfully.')
            return super().form_valid(form)
      
            
class WithdrawMoneyView(TransactionCreateMixin):
      form_class = WithdrawForm
      title = 'Withdraw Money'
      
      def get_initial(self):
            initial = {'transaction_type': WITHDRAW}
            return initial
      
      def form_valid(self, form):
            amount = form.cleaned_data.get('amount')
            account = self.request.user.account
            account.balance -= amount
            account.save(
                  update_fields = ['balance']
            )
            messages.success(self.request, f'BDT {amount} was withdrawn successfully.')
                  
            return super().form_valid(form)
           
            

class TransactionsReportView(LoginRequiredMixin, ListView):
      template_name = 'transactions/transaction_report.html'
      model = Transaction
      balance = 0
      title = 'Transaction Report'
      context_object_name = 'report_list'
      
      def get_queryset(self):
            # Get all transactions data from requested user
            queryset = super().get_queryset().filter(
                  account = self.request.user.account
            )
            
            # Get filtered transactions
            start_date_str = self.request.GET.get('start_date')
            end_date_str = self.request.GET.get('end_date')
            
            if start_date_str and end_date_str:
                  start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                  end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                  
                  # get data by using the filter
                  queryset = queryset.filter(timestamp__date__gte = start_date, timestamp__date__lte = end_date)
                  
                  # get final report
                  self.balance = Transaction.objects.filter(timestamp__date__gte = start_date, timestamp__date__lte = end_date).aggregate(Sum('amount'))['amount__sum']
            else:
                  self.balance = queryset.aggregate(Sum('amount'))['amount__sum']
                  
            return queryset.distinct()
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context.update({
                  'account': self.request.user.account,
                  'total_amount': self.balance,
            })
            return context