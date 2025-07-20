from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Comment

class PostListView(ListView):
    """عرض قائمة المقالات"""
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category').order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['featured_posts'] = Post.objects.filter(status='published', is_featured=True)[:3]
        return context

class PostDetailView(DetailView):
    """عرض تفاصيل المقال"""
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category')
    
    def get_object(self):
        obj = super().get_object()
        # زيادة عدد المشاهدات
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        
        # التعليقات المعتمدة
        context['comments'] = post.comments.filter(is_approved=True, parent=None).select_related('author')
        
        # مقالات مشابهة
        context['related_posts'] = Post.objects.filter(
            status='published',
            category=post.category
        ).exclude(id=post.id)[:3]
        
        # جميع الفئات
        context['categories'] = Category.objects.filter(is_active=True)
        
        return context

class CategoryPostsView(ListView):
    """عرض مقالات فئة معينة"""
    model = Post
    template_name = 'posts/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        category_slug = self.kwargs['slug']
        return Post.objects.filter(
            status='published',
            category__slug=category_slug
        ).select_related('author', 'category').order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['slug']
        context['category'] = get_object_or_404(Category, slug=category_slug)
        context['categories'] = Category.objects.filter(is_active=True)
        return context

def search_posts(request):
    """البحث في المقالات"""
    query = request.GET.get('q', '')
    posts = []
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__icontains=query),
            status='published'
        ).select_related('author', 'category').order_by('-published_at')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'posts': posts,
        'query': query,
        'categories': Category.objects.filter(is_active=True)
    }
    
    return render(request, 'posts/search_results.html', context)
