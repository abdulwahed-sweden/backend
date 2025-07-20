from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('search/', views.search_posts, name='search'),
    path('category/<slug:slug>/', views.CategoryPostsView.as_view(), name='category'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='detail'),
]
