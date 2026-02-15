from django.core.management import BaseCommand
from telegram_bot.main import TelegramBot


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Bot ishga tushdi")
        bot = TelegramBot()
        bot.run()