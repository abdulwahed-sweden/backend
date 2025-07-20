# apps/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import User
from .forms import UserRegistrationForm, UserProfileForm

class UserListView(ListView):
    """List all users"""
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        return User.objects.filter(is_active=True).order_by('-created_at')

class UserDetailView(DetailView):
    """User detail view"""
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

class UserRegistrationView(CreateView):
    """User registration view"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

class UserLoginView(LoginView):
    """User login view"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('users:profile')

class UserLogoutView(LogoutView):
    """User logout view"""
    next_page = reverse_lazy('home')

class UserProfileView(LoginRequiredMixin, TemplateView):
    """User profile view"""
    template_name = 'users/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context