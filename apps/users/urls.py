# apps/users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListView.as_view(), name='list'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='detail'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
]