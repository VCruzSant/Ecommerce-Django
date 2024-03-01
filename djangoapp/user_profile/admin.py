from django.contrib import admin
from user_profile.models import UserProfile

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = 'id', 'user', 'cpf', 'state'
    list_display_links = 'id',
    search_fields = 'id', 'user', 'cpf', 'state'
    list_per_page = 10
    ordering = '-id',
