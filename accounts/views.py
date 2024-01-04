from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView, LogoutView
from .models import UserBankAccount, UserAddress
from django.contrib import messages


# Create your views here.
class UserRegistrationView(FormView):
      template_name = 'accounts/user_registration.html'
      form_class = UserRegistrationForm
      success_url = reverse_lazy('login')
      
      
      def form_valid(self, form):
            print(form.cleaned_data)
            user = form.save()
            # login(self.request, user)
            # print(user)
            messages.success(self.request, 'Your account registration was successful. Please login to continue.')
            return super().form_valid(form)
            

class UserLoginView(LoginView):
      template_name = 'accounts/user_login.html'
      
      def get_success_url(self):
            messages.success(self.request, 'You are successfully logged in.')
            return reverse_lazy('home')
      
      
class UserLogoutView(LogoutView):
      def get_success_url(self):
            if self.request.user.is_authenticated:
                  logout(self.request)
                  messages.success(self.request, 'You are successfully logged out.')
            return reverse_lazy('home')
      
@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
      template_name = 'accounts/user_profile.html'

      def get(self, request, *args, **kwargs):
            user_bank_account = UserBankAccount.objects.get(user=request.user)
            user_address = UserAddress.objects.get(user=request.user)

            context = {
                  'user_bank_account': user_bank_account,
                  'user_address': user_address,
            }

            return render(request, self.template_name, context)
