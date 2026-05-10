from django.contrib import admin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type','phone_number']
    search_fields = ['username']
    list_filter = ['user_type']
    ordering = ['username']

