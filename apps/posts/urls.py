from django.urls import path
from django.views.generic import TemplateView

app_name = 'posts'

urlpatterns = [
    # Temporary placeholder views - will be replaced with proper views later
    path('', TemplateView.as_view(template_name='posts/post_list.html'), name='list'),
    path('<slug:slug>/', TemplateView.as_view(template_name='posts/post_detail.html'), name='detail'),
    path('category/<slug:slug>/', TemplateView.as_view(template_name='posts/category_posts.html'), name='category'),
]