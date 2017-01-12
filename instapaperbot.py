import logging
import re #searching url in message
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import instapaper #add link to instapaper
import config #временно загружаю логин-пароль ль instapaper

#логирование всех данных
def log_message(log_info):
    user_id = log_info['message']['chat']['id']
    user_username = log_info['message']['chat']['username']
    user_text = log_info['message']['text']
    debug_info = 'id:{} user:{} text:"{}"'.format(user_id,user_username,user_text)
    logging.info(debug_info)

#реакция при нажатии команды Start
def start (bot, update):
    bot.sendMessage(chat_id = update.message.chat_id, text = 'Hello, new user!')
    print ('New user')

#добавлении адреса в Instapaper конкретного человека
#пока можно установить собственный логин-пароль и постить туда адреса
def add_url_to_instapaper(chat_id,url):
    username = config.user
    password = config.password
    if str(chat_id) == config.id:
        instapaper.add_urls(username,password,url)
    else:
        print ("can't add link:{} from id:{}".format(url,chat_id))

#регулярное выражение для поиска URL в сообщении
def find_url(text):
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]|[А-Яа-я]))+')
    res = pattern.findall(text)
    return res

#основная функция по общению с пользователем
def conversation (bot, update):
    message_text = update['message']['text']
    clear_url = find_url(message_text)
    if len(clear_url) != 0:
        print ('url=',clear_url)
        if instapaper.authenticate(config.user,config.password):
            for single_url in clear_url:
                add_url_to_instapaper(update.message.chat_id,single_url)
            message_text = message_text.split()
            message_text = "Ok, link have been added,\n" + ' '.join(message_text[:7])
            bot.sendMessage(chat_id = update.message.chat_id,text = message_text)
        else:
            bot.sendMessage(chat_id = update.message.chat_id,text = "Thanks for the link, I soon learned to handle it,\n, I don't you your login password ")
    else:
        message = 'Sorry, I understand only text with links'
        bot.sendMessage(chat_id = update.message.chat_id,text = message)
    log_message(update)

#обработка всех остальных посылок, которые не текст
def reply_for_no_text_message(bot, update):
    bot.sendMessage(chat_id = update.message.chat_id,text = 'Sorry, I understand only text')
    log_message(update)
    logging.info('it was no text')


#реакция на неизвестные команды
def unknown(bot,update):
    bot.sendMessage(chat_id = update.message.chat_id,text = "I didn't understand that command.")

#основная функция программы
def main ():
    TOKEN = config.TOKEN
    #простое логгирование в файл
    logging.basicConfig(filename='info.log',level = logging.INFO,format='%(asctime)s - %(message)s')
    updater = Updater (token = TOKEN)
    dispatcher = updater.dispatcher
    #handlers
    start_handler = CommandHandler('start', start)
    conversation_handler = MessageHandler (Filters.text, conversation)
    unknown_handler = MessageHandler(Filters.command, unknown)
    reply_for_no_text_message_handler = MessageHandler(Filters.all, reply_for_no_text_message)
    #dispatchers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(reply_for_no_text_message_handler)
    #updater
    updater.start_polling()


if __name__ == '__main__':
    main()
