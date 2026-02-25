import os

from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from apps.bot.models import TelegramUser
from apps.user.models import User
from telegram_bot.text import name, phone_number, start, contact, warning_phone


class TelegramBot:

    def __init__(self):
        TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

        self.app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(MessageHandler(filters.TEXT | filters.CONTACT, self.message_handler))

    def run(self):
        self.app.run_polling()

    async def start(self, update, context):
        tg_user = update.effective_user
        bot_user = TelegramUser.objects.filter(chat_id=tg_user.id).first()

        if not bot_user:
            user = User.objects.create()
            TelegramUser.objects.create(
                chat_id=tg_user.id,
                username=tg_user.username,
                name=tg_user.full_name,
                user=user,
                state=TelegramUser.States.NAME,
            )
            await update.message.reply_text(text=name)
        else:
            await update.message.reply_text("Salom")

    async def message_handler(self, update, context):
        tg_user = update.effective_user
        bot_user = TelegramUser.objects.filter(chat_id=tg_user.id).first()

        if not bot_user:
            await update.message.reply_text(text=start)
            return

        if bot_user.state == TelegramUser.States.NAME:
            user = bot_user.user

            user.name = update.message.text
            user.save()

            bot_user.state = TelegramUser.States.PHONE
            bot_user.save()

            button = [
                [KeyboardButton(text=contact, request_contact=True)]
            ]
            reply_markup = ReplyKeyboardMarkup(
                keyboard=button,
                resize_keyboard=True,
                one_time_keyboard=True
            )

            await update.message.reply_text(
                text=phone_number,
                reply_markup=reply_markup
            )

            return

        if bot_user.state == TelegramUser.States.PHONE:

            phone = update.message.contact

            if not phone:
                await update.message.reply_text(text=warning_phone)
                return

            user = bot_user.user
            user.phone_number = phone.phone_number
            user.save()

            bot_user.state = TelegramUser.States.DONE
            bot_user.save()

            await update.message.reply_text("Raqamingiz saqlandi. Salom!")
            return

        if bot_user.state == TelegramUser.States.DONE:
            await update.message.reply_text("Salom")
