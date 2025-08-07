from django.contrib import admin
from .models import App_users
# Register your models here.

class UserTypeFilter(admin.SimpleListFilter):
    title = 'User type'
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        return [
            ('PUB', 'Publisher'),
            ('SUB', 'Viewer'),
            ('NaN', 'No Active'),
        ]
    def queryset(self, request, queryset):

        if self.value()=="PUB":
            return queryset.filter(user_type='PUB')
        if self.value()=="SUB":
            return queryset.filter(user_type='SUB')
        if self.value()=="NaN":
            return queryset.filter(user_type='NaN')
        return queryset

class AppUsersAdminModel(admin.ModelAdmin):
    model = App_users
    list_filter = ['is_active', UserTypeFilter]
    search_fields = ['email', 'username']
    list_display = ['username', 'email', 'is_publisher', 'user_type']

admin.site.register(App_users, AppUsersAdminModel)