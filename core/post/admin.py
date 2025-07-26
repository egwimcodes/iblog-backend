from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Category, Tag
from unfold.admin import ModelAdmin
# Register your models here.


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ['title', 'published_at']
    search_fields = ['title', 'description']
    list_filter = ['published_at']


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name']


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ['name']
