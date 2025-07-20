# apps/apis/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from apps.profiles.models import Profile, SocialLink
from apps.posts.models import Post, Category, Comment, Like
from .serializers import (
    UserSerializer, ProfileSerializer, SocialLinkSerializer,
    CategorySerializer, PostListSerializer, PostDetailSerializer,
    CommentSerializer, LikeSerializer
)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """User API ViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get', 'put'])
    def me(self, request):
        """Get or update current user"""
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(viewsets.ModelViewSet):
    """Profile API ViewSet"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return Profile.objects.filter(is_public=True)
        return Profile.objects.all()
    
    @action(detail=False, methods=['get', 'put'])
    def me(self, request):
        """Get or update current user's profile"""
        profile, created = Profile.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ModelViewSet):
    """Category API ViewSet"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class PostViewSet(viewsets.ModelViewSet):
    """Post API ViewSet"""
    queryset = Post.objects.filter(status='published').order_by('-published_at')
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, slug=None):
        """Like/unlike a post"""
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        
        if not created:
            like.delete()
            post.likes_count = max(0, post.likes_count - 1)
            post.save(update_fields=['likes_count'])
            return Response({'liked': False, 'likes_count': post.likes_count})
        else:
            post.likes_count += 1
            post.save(update_fields=['likes_count'])
            return Response({'liked': True, 'likes_count': post.likes_count})
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured posts"""
        featured_posts = Post.objects.filter(status='published', is_featured=True)
        serializer = self.get_serializer(featured_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get posts by category"""
        category_slug = request.query_params.get('category')
        if category_slug:
            posts = self.queryset.filter(category__slug=category_slug)
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category parameter required'}, 
                       status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    """Comment API ViewSet"""
    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)