from django.contrib import admin
from unfold.admin import ModelAdmin

from core.account.models import IBlogUser
# Register your models here.


@admin.register(IBlogUser)
class IBlogUserAdmin(ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_staff']



