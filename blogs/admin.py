from django.contrib import admin
from .models import  BlogPost, Category
from unfold.admin import ModelAdmin
# Register your models here.


@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
    list_display = ['title', 'published_date']
    search_fields = ['title', 'description']
    list_filter = ['published_date']


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['category']
