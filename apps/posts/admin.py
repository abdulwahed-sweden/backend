from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Category, Post, Comment, Like

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category Admin"""
    
    list_display = ('name', 'slug', 'posts_count', 'color_display', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    
    def posts_count(self, obj):
        return obj.posts.filter(status='published').count()
    posts_count.short_description = 'Published Posts'
    
    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; width: 20px; height: 20px; display: inline-block; border-radius: 3px; border: 1px solid #ddd;"></span> {}',
            obj.color, obj.color
        )
    color_display.short_description = 'Color'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post Admin"""
    
    list_display = ('title', 'author', 'category', 'status', 'is_featured', 'views_count', 'likes_count', 'comments_count', 'published_at')
    list_filter = ('status', 'is_featured', 'category', 'created_at', 'published_at')
    search_fields = ('title', 'content', 'author__username', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    list_editable = ('status', 'is_featured')
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('content', 'excerpt', 'featured_image')
        }),
        ('Settings', {
            'fields': ('status', 'is_featured', 'tags')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views_count', 'likes_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('views_count', 'likes_count', 'created_at', 'updated_at')
    
    def comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()
    comments_count.short_description = 'Comments'
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['make_published', 'make_draft', 'make_featured']
    
    def make_published(self, request, queryset):
        queryset.update(status='published')
    make_published.short_description = "Mark selected posts as published"
    
    def make_draft(self, request, queryset):
        queryset.update(status='draft')
    make_draft.short_description = "Mark selected posts as draft"
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = "Mark selected posts as featured"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment Admin"""
    
    list_display = ('post_title', 'author', 'content_preview', 'is_approved', 'is_reply', 'created_at')
    list_filter = ('is_approved', 'created_at', 'post__category')
    search_fields = ('content', 'author__username', 'post__title')
    actions = ['approve_comments', 'disapprove_comments']
    list_per_page = 30
    
    def post_title(self, obj):
        return obj.post.title[:50]
    post_title.short_description = 'Post'
    post_title.admin_order_field = 'post__title'
    
    def content_preview(self, obj):
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def is_reply(self, obj):
        return obj.parent is not None
    is_reply.boolean = True
    is_reply.short_description = 'Reply'
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Approve selected comments'
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = 'Disapprove selected comments'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Like Admin"""
    
    list_display = ('post_title', 'user', 'created_at')
    list_filter = ('created_at', 'post__category')
    search_fields = ('post__title', 'user__username')
    list_per_page = 50
    
    def post_title(self, obj):
        return obj.post.title[:50]
    post_title.short_description = 'Post'
    post_title.admin_order_field = 'post__title'
