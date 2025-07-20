from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, SocialLink

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1
    fields = ('platform', 'url', 'is_active')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile Admin"""
    
    list_display = ('user_display', 'location', 'website_link', 'is_public', 'avatar_preview', 'social_links_count', 'created_at')
    list_filter = ('is_public', 'created_at', 'birth_date')
    search_fields = ('user__username', 'user__email', 'bio', 'location')
    inlines = [SocialLinkInline]
    list_per_page = 20
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('bio', 'avatar', 'location', 'website', 'birth_date', 'phone')
        }),
        ('Settings', {
            'fields': ('is_public',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def user_display(self, obj):
        return f"{obj.user.username} ({obj.user.email})"
    user_display.short_description = 'User'
    user_display.admin_order_field = 'user__username'
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;">',
                obj.avatar.url
            )
        return "No Avatar"
    avatar_preview.short_description = 'Avatar'
    
    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.website, obj.website[:30])
        return "No Website"
    website_link.short_description = 'Website'
    
    def social_links_count(self, obj):
        return obj.social_links.filter(is_active=True).count()
    social_links_count.short_description = 'Social Links'

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """Social Link Admin"""
    
    list_display = ('profile_user', 'platform', 'url_link', 'is_active', 'created_at')
    list_filter = ('platform', 'is_active', 'created_at')
    search_fields = ('profile__user__username', 'url', 'platform')
    list_per_page = 30
    
    def profile_user(self, obj):
        return obj.profile.user.username
    profile_user.short_description = 'User'
    profile_user.admin_order_field = 'profile__user__username'
    
    def url_link(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url[:40])
    url_link.short_description = 'URL'
