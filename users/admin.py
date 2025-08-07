from django.contrib import admin
from .models import App_users
# Register your models here.


class AppUsersAdminModel(admin.ModelAdmin):
    model = App_users
    list_filter = ['is_publisher']
    search_fields = ['email', 'username']
    list_display = ['username', 'email', 'is_publisher', 'user_type']

admin.site.register(App_users, AppUsersAdminModel)