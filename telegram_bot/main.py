import os

from telegram.ext import ApplicationBuilder, CommandHandler

from apps.bot.models import TelegramUser

NAME, PHONE_NUMBER = range(2)


class TelegramBot:

    def __init__(self):
        TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

        self.app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        self.app.add_handler(CommandHandler("start", self.start))

    def run(self):
        self.app.run_polling()

    async def start(self, update, context):
        user = update.effective_user
        bot_user = TelegramUser.objects.filter(chat_id=user.id).first()

        if not bot_user:
            await update.message.reply_text(
                text="Ism Familiyangizni kiriting."
            )
