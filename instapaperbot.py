from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters


def start (bot, update):
    bot.sendMessage(chat_id = update.message.chat_id, text = 'Hello')
    print ('yes')

def echo (bot, update):
    bot.sendMessage(chat_id = update.message.chat_id,text = update.message.text)
    print (bot)
    print (update)

def forward_to_instapapper(bot,update):
    print (update)

def unknown(bot,update):
    bot.sendMessage(chat_id = update.message.chat_id,text = "I didn't understand that command.")

def main ():
    with open ('TOKEN.txt') as f:
        a = f.read()
        TOKEN = a.replace('\n','')
    updater = Updater (token = TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler (Filters.text, echo)
    forward_handler = MessageHandler(Filters.forwarded,forward_to_instapapper)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(forward_to_instapapper)
    updater.start_polling()



if __name__ == '__main__':
    main()
