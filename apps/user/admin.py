from django.contrib import admin

from apps.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'phone_number',
    ]

    search_fields = [
        'name',
        'phone_number',
    ]
