import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Assalomu alaykum! Kanalga xush kelibsiz!")

# Welcome yangi foydalanuvchi
def welcome(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        bot.send_message(chat_id=update.message.chat_id, text=f"{member.full_name}, kanalimizga xush kelibsiz!")

# Broadcast (admin)
def broadcast(update: Update, context: CallbackContext):
    if str(update.effective_user.id) == str(os.environ.get("ADMIN_ID")):
        msg = " ".join(context.args)
        bot.send_message(chat_id=CHANNEL_ID, text=msg)
    else:
        update.message.reply_text("Siz admin emassiz!")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
dispatcher.add_handler(CommandHandler("broadcast", broadcast, pass_args=True))

updater.start_polling()
updater.idle()
