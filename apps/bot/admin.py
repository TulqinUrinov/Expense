from django.contrib import admin

from apps.bot.models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'chat_id',
        'username',
        'name',
    )

    search_fields = (
        'chat_id',
        'name',
        'username',
    )
