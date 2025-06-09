from django.contrib import admin
from .models import IBlogUser
from unfold.admin import ModelAdmin
# Register your models here.


@admin.register(IBlogUser)
class IBlogUserAdmin(ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_staff']
