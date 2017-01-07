import logging
import re
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

def log_message(log_info):
    user_id = log_info['message']['chat']['id']
    user_username = log_info['message']['chat']['username']
    user_text = log_info['message']['text']
    debug_info = 'id:{} user:{} text:"{}"'.format(user_id,user_username,user_text)
    #print (debug_info)
    logging.info(debug_info)

def start (bot, update):
    bot.sendMessage(chat_id = update.message.chat_id, text = 'Hello')
    print ('yes')

def find_url(text):
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    res = pattern.findall(text)
    return res


def conversation (bot, update):
    message_text = update['message']['text']
    clear_url = find_url(message_text)
    if len(clear_url) != 0:
        print ('url=',clear_url)
        bot.sendMessage(chat_id = update.message.chat_id,text = 'Thanks for the link, I soon learned to handle it')
    else:
        bot.sendMessage(chat_id = update.message.chat_id,text = update.message.text)
    log_message(update)

def forward_to_instapapper(bot,update):
    print ('forward message')
    message_text = update['message']['text']
    clear_url = find_url(message_text)
    print (clear_url)
    log_message(update)


def unknown(bot,update):
    bot.sendMessage(chat_id = update.message.chat_id,text = "I didn't understand that command.")

def main ():
    with open ('TOKEN.txt', encoding='utf8') as f:
        a = f.read()
        TOKEN = a.replace('\n','')
    #простое логгирование в файл
    logging.basicConfig(filename='info.log',level = logging.INFO,format='%(asctime)s - %(message)s')
    updater = Updater (token = TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    conversation_handler = MessageHandler (Filters.text, conversation)
    forward_handler = MessageHandler(Filters.forwarded,forward_to_instapapper)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(forward_handler)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()



if __name__ == '__main__':
    main()
