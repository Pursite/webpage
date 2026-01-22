from django.contrib import admin
from .models.user_model import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'get_username', 'full_name', 'is_verified', 'created_at')

    search_fields = ('phone_number', 'username__username', 'full_name', 'national_code')

    list_filter = ('is_verified', 'created_at')

    fieldsets = (
        ('Account Info', {
            'fields': ('username', 'phone_number', 'is_verified')
        }),
        ('Personal Info', {
            'fields': ('full_name', 'national_code', 'email', 'address')
        }),
    )

    @admin.display(description='Username')
    def get_username(self, obj):
        return obj.user.username