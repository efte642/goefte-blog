from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Post, Category
from taggit.models import Tag


class HomeView(ListView):
    model = Post
    template_name = "core_app/index.html"  # root templates folder
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(published=True).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "hero_posts": Post.objects.filter(section="hero", published=True).order_by("-created_at")[:4],
            "featured_posts": Post.objects.filter(section="featured", published=True).order_by("-created_at")[:4],
            "popular_posts": Post.objects.filter(section="popular", published=True).order_by("-created_at")[:6],
            "community_posts": Post.objects.filter(section="community", published=True).order_by("-created_at")[:4],
            "recent_posts": Post.objects.filter(published=True).order_by("-created_at")[:6],
            "categories": Category.objects.all(),
            "meta_title": "Goefte Magazine – Lifestyle, Travel, Tech & Culture for USA and Canada",
            "meta_description": "Goefte Magazine delivers trending stories on lifestyle, travel, tech, wellness, and culture for readers in the USA and Canada.",
            "meta_keywords": "Goefte, USA magazine, Canada magazine, online magazine, lifestyle trends, tech news, travel blog, wellness tips",
            "meta_image": None,
        })
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "core_app/post_detail.html"  # root templates folder
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context.update({
            "hero_posts": Post.objects.filter(section="hero", published=True),
            "featured_posts": Post.objects.filter(section="featured", published=True),
            "recent_posts": Post.objects.filter(published=True).exclude(id=post.id).order_by("-created_at")[:5],
            "related_posts": Post.objects.filter(category=post.category, published=True)
                                        .exclude(id=post.id).order_by("-created_at")[:3],
            "categories": Category.objects.all(),
        })
        return context


class CategoryPostView(ListView):
    model = Post
    template_name = "core_app/category_posts.html"  # root templates folder
    context_object_name = "posts"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return Post.objects.filter(category__slug=slug, published=True).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        category = get_object_or_404(Category, slug=slug)
        context.update({
            "category": category,
            "meta_title": f"{category.name} – Goefte Magazine",
            "meta_description": f"Read all articles about {category.name} on Goefte Magazine.",
            "meta_keywords": f"{category.name}, Goefte Magazine, USA, Canada",
            "meta_image": getattr(category, "image", None),
            "recent_posts": Post.objects.filter(published=True).order_by("-created_at")[:5],
        })
        return context


class TagPostView(ListView):
    template_name = "core_app/tag_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return Post.objects.filter(tags__slug=slug, published=True).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        tag = Tag.objects.filter(slug=slug).first()
        context.update({
            "tag": tag or slug,
            "meta_title": f"Posts tagged '{slug}' – Goefte Magazine",
            "meta_description": f"Explore all posts tagged with '{slug}' on Goefte Magazine.",
            "meta_keywords": f"{slug}, Goefte Magazine, USA, Canada",
            "meta_image": None,
            "recent_posts": Post.objects.filter(published=True).order_by("-created_at")[:5],
        })
        return context
