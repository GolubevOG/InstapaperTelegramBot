from telegram.ext import Updater
from telegram.ext import CommandHandler

def start (bot, update):
    bot.sendMessage(chat_id = update.message.chat_id, text = 'Hello')




with open ('../TOKEN_INSTAPAPERBOT.txt') as f:
    a = f.read()
    TOKEN = a [:-1]
updater = Updater (token = TOKEN)
start_handler = CommandHandler('start', start)
updater.start_polling()
