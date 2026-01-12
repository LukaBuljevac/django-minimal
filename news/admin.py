from django.contrib import admin
from .models import Category, News, NewsFavorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at"]
    list_filter = ["created_at", "categories"]
    search_fields = ["title", "text"]
    filter_horizontal = ["categories"]


@admin.register(NewsFavorite)
class NewsFavoriteAdmin(admin.ModelAdmin):
    list_display = ["user", "news", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__username", "news__title"]
