import logging
import re #searching url in message
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import instapaper # should be installed as pip install git+https://github.com/rsgalloway/instapaper
import config #временно загружаю логин-пароль для instapaper
from db import db_session, User #подключаю базу данных
import urllib.parse


#логирование всех данных
def log_message(log_info):
    user_id = log_info['message']['chat']['id']
    user_username = log_info['message']['chat']['username']
    user_text = log_info['message']['text']
    debug_info = 'id:{} user:{} text:"{}"'.format(user_id,user_username,user_text)
    logging.info(debug_info)

#пользователь заноситься в базу данных, при активации команды START
def add_new_user_to_db(user_info):
    user_id = user_info['message']['chat']['id']
    user_username = user_info['message']['chat']['username']
    new_user = User()
    
    user_in_db = new_user.query.filter(User.user_id.like(user_id)).first()
    if user_in_db == None:
        new_user.user_id = user_id
        new_user.user_nickname = user_username
        db_session.add (new_user)
        db_session.commit()
        bot.sendMessage(chat_id = update.message.chat_id, text = 'Hello, new user!')
    else:
        new_start_message = 'Hello ' + user_username
        bot.sendMessage(chat_id = update.message.chat_id, text = new_start_message)



#реакция при нажатии команды Start
#тут нужно добавить добавление пользователя в базу пользователей
def start (bot, update):
    add_new_user_to_db(update)
    log_message(update)
    logging.info('\n!!New User!!\n')

#реакия при нажатии команды info
def info_message(bot, update):
    bot.sendMessage(chat_id = update.message.chat_id, text = '''bot sends a link to your Instapaper.
But you have to login.
Please use command "login"''')

# logging out
# TODO3: doesn't work. WHY?
def logout(bot, update, user_data):
    user_data = {0: 0}
    bot.sendMessage(chat_id = update.message.chat_id, text = 'Logged out!')

# authentication
# TODO4: passwords should not be saved in chat history! https://github.com/yagop/node-telegram-bot-api/issues/143
def take_user_login_password(bot, update, args, user_data):
    try:
        if user_data.get('token'):
            msg = 'Already logged in as %s. Use /logout first if you want to change user.' % user_data['username']
        else:
            # TODO1: check if we have token for update.message.from_user.id (i.e. telegram id of current user) (see TODO2)
            # check is some credentials are passed
            if len(args) != 2:
                msg = 'Please enter credentials as "/login username password". We don\'t save them'
            else:
                I = instapaper.Instapaper(config.oauth_token, config.oauth_secret)
                try:
                    # logging in
                    I.login(args[0], args[1])
                    # TODO2: save token to DB
                    user_data['token'] = dict(urllib.parse.parse_qsl(str(I.token)))
                    user_data['login'] = I

                    #getting user data
                    user = I.user().get('username')
                    user_data['username'] = user
                    msg = 'Logged in as %s!' % user
                except KeyError:
                    msg = 'Incorrect credentials!'

    except Exception as e:
        msg = 'There was an error: %s' % str(e)

    bot.sendMessage(chat_id = update.message.chat_id, text = msg)

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
        #print ('url=',clear_url)
        if instapaper.authenticate(config.user,config.password):
            for single_url in clear_url:
                add_url_to_instapaper(update.message.chat_id,single_url)
            message_text = message_text.split()
            index_of_first_url_in_text = message_text.index(clear_url[0])
            message_text = "Ok, link have been added,\nText: " + ' '.join(message_text[:index_of_first_url_in_text])
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
    info_handler = CommandHandler('info', info_message)
    login_handler = CommandHandler('login', take_user_login_password, pass_args=True, pass_user_data=True)
    logout_handler = CommandHandler('logout', logout, pass_user_data=True)
    conversation_handler = MessageHandler (Filters.text, conversation)
    unknown_handler = MessageHandler(Filters.command, unknown)
    reply_for_no_text_message_handler = MessageHandler(Filters.all, reply_for_no_text_message)

    #dispatchers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(login_handler)
    dispatcher.add_handler(logout_handler)
    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(reply_for_no_text_message_handler)
    #updater
    updater.start_polling()


if __name__ == '__main__':
    main()
