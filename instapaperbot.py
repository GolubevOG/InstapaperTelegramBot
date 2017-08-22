import logging
import re  # searching url in message
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import config  # временно загружаю ТОKEN
import instawrapper as iw
import db

# логирование всех данных
def log_message(log_info):
    user_id = log_info['message']['chat']['id']
    user_username = log_info['message']['chat']['username']
    user_text = log_info['message']['text']
    debug_info = 'id:{} user:{} text:"{}"'.format(user_id, user_username, user_text)
    logging.info(debug_info)

'''
# пользователь заносится в базу данных, при активации команды START 
# тестовая функция
def add_new_user_to_db(user_id):
    try: 
        db.User.add_user_when_start(user_id)
    except Exception as e:
        msg = 'Error start' + str(e)
        logging.info(msg)
'''
     
# реакция при нажатии команды Start
# тут нужно добавить добавление пользователя в базу пользователей
def start(bot, update):
    user_id = int(update.message.from_user.id)
    if not db.User.is_user_login(user_id): 
        #add_new_user_to_db(user_id)
        msg = "Please login first (/login command)"
    else:
        msg = "You can add links"
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)
    log_message(update)
    logging.info('\n!!New User!!\n')


# реакия при нажатии команды info
def info_message(bot, update):
    if not db.User.is_user_login(int(update.message.from_user.id)): 
        bot.sendMessage(chat_id=update.message.chat_id, text='''bot sends a link to your Instapaper.\
                                                                But you have to login.\
                                                                Please use command "login"''')
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='''thank you for using this bot''')


# logout
def logout(bot, update):
    try:
        if db.User.is_user_login(int(update.message.from_user.id)): 
            db.User.delete(int(update.message.from_user.id))
        msg = 'Logged out!'
    except Exception as e:
        msg = 'Something has gone wrong!'
        logging.info('error in logout: {}'.format(e))
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)


# authentication
# TODO4: passwords should not be saved in chat history! https://github.com/yagop/node-telegram-bot-api/issues/143
def login(bot, update, args, user_data):
    if not db.User.is_user_login(int(update.message.from_user.id)): 
        try:
            wrapper = iw.Ipaper()
            loggedin, msg = wrapper.login(update.message.from_user.id, args)

            if loggedin == 1:
                user_data['wrapper'] = wrapper

        except Exception as e:
            msg = 'Something has gone wrong!'
            #msg = 'There was an error: {}'.format(str(e))
            logging.info('error in login: {}'.format(e))
    else:
        msg = 'You already login!'

    bot.sendMessage(chat_id=update.message.chat_id, text=msg)
    log_message(update)


def relogin_after_disconnect(user_data, user_id):
    #проверка, если человек залогинин, но временных данных о нем нет
    #значит сервер был перегружен
    #обновление временных данных за счет перелогирования
    if db.User.is_user_login(user_id) and user_data.get('wrapper', '*') == '*':
        try:
            wrapper = iw.Ipaper()
            wrapper.login_with_token(user_id)
            user_data['wrapper'] = wrapper
        except Exception as e:
            msg = 'Something has gone wrong!'
            logging.info('error in login: {}'.format(e))



def add_link(url, user_data, user_id):
    msg = 'Error'
    #проверка на актуальность данных в памяти
    relogin_after_disconnect(user_data, user_id)
    
    #добавление ссылки 
    try:
        user_data.get('wrapper').bookmark({"url": url})
        msg = 'Saved!'
    except Exception as e:
        print (e)
        msg = str(e) + '- error add link'
    return msg


# регулярное выражение для поиска URL в сообщении
def find_url(text):
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]|[А-Яа-я]))+')
    res = pattern.findall(text)
    return res
    
#отправляется текст, находится ссылка и добавлается в instapaper
def search_and_add_links (bot, update, user_data, message_text):
    user_id = int(update.message.from_user.id)
    if db.User.is_user_login(user_id):
        clear_url = find_url(message_text)
        if len(clear_url) != 0:
            for single_url in clear_url:
                # why is clear_url a dict? it's very ulikely that someone will add more that one URL in a single message
                msg = add_link(single_url, user_data, user_id)
        else:
            msg = 'Sorry, I understand only text with links'
        log_message(update)
    else:
        msg = 'Please log in!'
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)
    

# основная функция по общению с пользователем
def conversation(bot, update, user_data):
    text_from_message = update['message']['text']
    search_and_add_links(bot, update, user_data, text_from_message)
    



# обработка всех остальных посылок, которые не текст
def reply_for_no_text_message(bot, update, user_data):
    text_from_message = update['message']['caption']
    if text_from_message != None:
        search_and_add_links(bot, update, user_data, text_from_message)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text='Sorry, I understand only text.')
        log_message(update)
        logging.info('it was no text')
    

# реакция на неизвестные команды
def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I didn't understand that command.")
    log_message(update)

# основная функция программы


def main():
    #токен от бота
    TOKEN = config.TOKEN
    # простое логгирование в файл
    logging.basicConfig(filename='info.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    # handlers
    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler('info', info_message)
    login_handler = CommandHandler('login', login, pass_args=True, pass_user_data=True)
    logout_handler = CommandHandler('logout', logout)
    conversation_handler = MessageHandler(Filters.text, conversation, pass_user_data=True)
    unknown_handler = MessageHandler(Filters.command, unknown)
    reply_for_no_text_message_handler = MessageHandler(Filters.all, reply_for_no_text_message, pass_user_data=True)

    # dispatchers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(login_handler)
    dispatcher.add_handler(logout_handler)
    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(reply_for_no_text_message_handler)
    
    # updater
    updater.start_polling()


if __name__ == '__main__':
    main()
