import logging
import re  # searching url in message
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import instapaper  # should be installed as pip install git+https://github.com/rsgalloway/instapaper
import config  # временно загружаю логин-пароль для instapaper
from db import db_session, User  # подключаю базу данных
import urllib.parse
import instawrapper as iw

# логирование всех данных


def log_message(log_info):
    user_id = log_info['message']['chat']['id']
    user_username = log_info['message']['chat']['username']
    user_text = log_info['message']['text']
    debug_info = 'id:{} user:{} text:"{}"'.format(user_id, user_username, user_text)
    logging.info(debug_info)

# пользователь заносится в базу данных, при активации команды START


def add_new_user_to_db(user_info):
    user_id = user_info['message']['chat']['id']
    user_username = user_info['message']['chat']['username']
    new_user = User()
    user_in_db = new_user.query.filter(User.user_id.like(user_id)).first()
    if user_in_db is None:
        new_user.user_id = user_id
        new_user.user_nickname = user_username
        db_session.add(new_user)
        db_session.commit()
        bot.sendMessage(chat_id=update.message.chat_id, text='Hello, new user!')
    else:
        new_start_message = 'Hello ' + user_username
        bot.sendMessage(chat_id=update.message.chat_id, text=new_start_message)


# реакция при нажатии команды Start
# тут нужно добавить добавление пользователя в базу пользователей
def start(bot, update):
    #add_new_user_to_db(update)
    msg = "PLease login first (/login command)"
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)
    log_message(update)
    logging.info('\n!!New User!!\n')

# реакия при нажатии команды info


def info_message(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='''bot sends a link to your Instapaper.
But you have to login.
Please use command "login"''')

# logging out
# TODO3: doesn't work. WHY?


def logout(bot, update, user_data):
    try:
        user_data.pop('wrapper', None)
        msg = 'Logged out!'
    except:
        msg = 'Something has gone wrong!'
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

# authentication
# TODO4: passwords should not be saved in chat history! https://github.com/yagop/node-telegram-bot-api/issues/143


def login(bot, update, args, user_data):
    
    try:
        if user_data.get('wrapper', '*') == '*':
            user_data['wrapper'] = iw.Ipaper()

        msg = user_data['wrapper'].login(update.message.from_user.id, args)

    except Exception as e:
        msg = 'There was an error: {}'.format(str(e))
        log_message(update, str(e))

    print (user_data)


    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

# добавлении адреса в Instapaper конкретного человека
# пока можно установить собственный логин-пароль и постить туда адреса


def bookmark(url, user_data):
    msg = 'No'
    if user_data.get('wrapper', '*') != '*':
        try:
            b = user_data.get('wrapper').bookmark({"url": url})
            # b.save()
            msg = 'Saved!'
        except Exception as e:
            msg = str(e) + '12'

    return msg


# регулярное выражение для поиска URL в сообщении
def find_url(text):
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]|[А-Яа-я]))+')
    res = pattern.findall(text)
    return res


# основная функция по общению с пользователем
def conversation(bot, update, user_data):
    try:
        if user_data.get('wrapper', '*') == '*':
            # try to log in with saved token
            user_data['wrapper'] = iw.Ipaper()
            user_data['wrapper'].login_with_token(update.message.from_user.id)

        print(user_data['wrapper'])

        message_text = update['message']['text']
        clear_url = find_url(message_text)
        if len(clear_url) != 0:
            if 1 == 1:  # TODO: check if authenticated
                for single_url in clear_url:
                    # why is clear_url a dict? it's very ulikely that someone will add more that one URL in a single message
                    msg = bookmark(single_url, user_data)
            else:
                msg = "PLease login first (/login command). But thanks for the link anyway :)"
        else:
            msg = 'Sorry, I understand only text with links'
            bot.sendMessage(chat_id=update.message.chat_id, text=msg)
        log_message(update)
    except Exception as e:
        msg = str(e)
    log_message(update)
    print (user_data)

    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

# обработка всех остальных посылок, которые не текст


def reply_for_no_text_message(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='Sorry, I understand only text.')
    log_message(update)
    logging.info('it was no text')


# реакция на неизвестные команды
def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I didn't understand that command.")
    log_message(update)

# основная функция программы


def main():
    TOKEN = config.TOKEN
    # простое логгирование в файл
    logging.basicConfig(filename='info.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    # handlers
    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler('info', info_message)
    login_handler = CommandHandler('login', login, pass_args=True, pass_user_data=True)
    logout_handler = CommandHandler('logout', logout, pass_user_data=True)
    conversation_handler = MessageHandler(Filters.text, conversation, pass_user_data=True)
    unknown_handler = MessageHandler(Filters.command, unknown)
    reply_for_no_text_message_handler = MessageHandler(Filters.all, reply_for_no_text_message)

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
