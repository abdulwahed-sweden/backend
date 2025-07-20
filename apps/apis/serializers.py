# apps/apis/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.profiles.models import Profile, SocialLink
from apps.posts.models import Post, Category, Comment, Like

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    full_name = serializers.ReadOnlyField()
    display_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'full_name', 'display_name', 'is_verified', 'created_at']
        read_only_fields = ['id', 'is_verified', 'created_at']

class SocialLinkSerializer(serializers.ModelSerializer):
    """Social link serializer"""
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    
    class Meta:
        model = SocialLink
        fields = ['id', 'platform', 'platform_display', 'url', 'is_active']

class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer"""
    user = UserSerializer(read_only=True)
    social_links = SocialLinkSerializer(many=True, read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'avatar', 'location', 'website', 
                 'birth_date', 'phone', 'is_public', 'social_links', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'color', 
                 'is_active', 'posts_count', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']
    
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published').count()

class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer"""
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'parent', 'replies', 
                 'is_approved', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

class PostListSerializer(serializers.ModelSerializer):
    """Post list serializer (minimal fields)"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tag_list = serializers.ReadOnlyField()
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'category', 'excerpt', 
                 'featured_image', 'status', 'is_featured', 'tag_list',
                 'views_count', 'likes_count', 'comments_count', 
                 'published_at', 'created_at']
    
    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()

class PostDetailSerializer(serializers.ModelSerializer):
    """Post detail serializer (all fields)"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tag_list = serializers.ReadOnlyField()
    comments = CommentSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'category', 'content', 
                 'excerpt', 'featured_image', 'status', 'is_featured', 
                 'tag_list', 'meta_description', 'views_count', 'likes_count',
                 'comments', 'is_liked', 'published_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'author', 'views_count', 'likes_count',
                           'published_at', 'created_at', 'updated_at']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

class LikeSerializer(serializers.ModelSerializer):
    """Like serializer"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']