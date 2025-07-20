# apps/posts/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    """Post categories"""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('posts:category', kwargs={'slug': self.slug})

class Post(models.Model):
    """Blog post model"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text='Short description')
    featured_image = models.ImageField(upload_to='posts/', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags')
    meta_description = models.CharField(max_length=160, blank=True, help_text='SEO meta description')
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})
    
    @property
    def tag_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

class Comment(models.Model):
    """Post comments"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    @property
    def is_reply(self):
        return self.parent is not None

class Like(models.Model):
    """Post likes"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'likes'
        unique_together = ['post', 'user']
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
    
    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'