import os

from telegram.ext import ApplicationBuilder, CommandHandler
from telegram.request import HTTPXRequest


class TelegramBot:

    def __init__(self):
        TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

        # Timeout sozlamalari
        request = HTTPXRequest(
            connect_timeout=30.0,
            read_timeout=30.0,
            write_timeout=30.0,
            pool_timeout=30.0,
        )

        self.app = ApplicationBuilder() \
            .token(TELEGRAM_BOT_TOKEN) \
            .request(request) \
            .build()

        self.app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        self.app.add_handler(CommandHandler("start", self.start))

    def run(self):
        self.app.run_polling()

    async def start(self, update, context):
        user = update.effective_user

        await update.message.reply_text(f"Salom {user.full_name}")
