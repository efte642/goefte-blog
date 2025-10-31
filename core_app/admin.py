from django.contrib import admin
from .models import Category, Post
from taggit.admin import TagAdmin
from taggit.models import Tag

# -----------------------------
# Taggit: Custom Tag Admin
# -----------------------------
# Unregister default Tag if already registered
try:
    admin.site.unregister(Tag)
except admin.sites.NotRegistered:
    pass

# Register Tag with autocomplete support
@admin.register(Tag)
class CustomTagAdmin(TagAdmin):
    search_fields = ('name',)

# -----------------------------
# Category Admin
# -----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)

# -----------------------------
# Post Admin
# -----------------------------
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'section', 'published', 'views', 'created_at')
    list_filter = ('category', 'section', 'published', 'created_at')
    search_fields = ('title', 'content', 'meta_title', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('tags',)
    readonly_fields = ('views', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'image', 'content', 'tags', 'section', 'published')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Timestamps & Stats', {
            'fields': ('views', 'created_at', 'updated_at')
        }),
    )

    # Optional: highlight published posts in admin list
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category')
