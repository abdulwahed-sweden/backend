
from django.urls import path
from django.views.generic import TemplateView

app_name = 'profiles'

urlpatterns = [
    # Temporary placeholder views - will be replaced with proper views later
    path('', TemplateView.as_view(template_name='profiles/profile_list.html'), name='list'),
    path('<int:pk>/', TemplateView.as_view(template_name='profiles/profile_detail.html'), name='detail'),
]
