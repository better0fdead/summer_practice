import time
from dotenv import load_dotenv
import os
import flask
import telebot

import meta
import checker
import data_base


app = flask.Flask(__name__)

load_dotenv()
bot = telebot.TeleBot(os.getenv('API_TOKEN'))
db = data_base.DataBase()
check = checker.Checker()


@app.route(os.getenv("WEBHOOK_URL_PATH"), methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Здравствуйте!\n' + meta.HELP_MSG)


# Вызов справки.
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, meta.HELP_MSG)


# Получение новых сообщений.
@bot.message_handler(commands=['update'])
def send_update(message):
    bot.send_message(message.chat.id, 'Ваш запрос обрабатывается.')
    if not db.if_id_exist(message.chat.id):
        bot.send_message(message.chat.id, 'Войдите в аккаунт: /login')
        return
    login, password = db.get_login_password(message.chat.id)
    if check.login(login, password):
        bot.send_message(
            message.chat.id, 'Не удалось войти в почту.')
        return
    count = check.get_count()
    bot.send_message(
        message.chat.id, 'Количество новых писем: {}.'.format(count))
    if count > 0:
        last_msg = check.get_last(count)
        check.select_all_as_readed()
        for i in range(count):
            letter = 'Отправитель: ' + last_msg[i].sender + \
                '\n\nТема: ' + (last_msg[i].theme if last_msg[i].theme != '' else '<Без темы>') + \
                '\n\nПисьмо:\n' + last_msg[i].content + (
                    '\n\nВ письме есть прикрепленные файлы.' if last_msg[i].attachment else '')
            bot.send_message(message.chat.id, letter)
    check.exit()


# Авторизация (все 3 функции).
try_login = False
try_pass = False
login = ''
@bot.message_handler(commands=['login'])
def send_login(message):
    global try_login, try_pass, login
    if db.if_id_exist(message.chat.id):
        bot.send_message(message.chat.id, 'Вы уже вошли.')
        return
    try_login = True
    login = ''
    try_pass = False
    bot.send_message(message.chat.id, 'Введите логин:')


@bot.message_handler(func=lambda m: try_login)
def get_login(message):
    global try_login, try_pass, login
    try_login = False
    try_pass = True
    login = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль:')


@bot.message_handler(func=lambda m: try_pass)
def get_pass(message):
    global try_pass, login
    try_pass = False
    try_login = False
    password = message.text.strip()
    bot.send_message(message.chat.id, 'Проверка данных.')
    if check.login(login, password):
        bot.send_message(
            message.chat.id, 'Не удалось войти в почту. \nПопробуйте снова: /login')
        return
    db.add_field(message.chat.id, login, password)
    bot.send_message(message.chat.id, 'Готово.')
    login = ''
    check.exit()


# Выход из учетной записи.
@bot.message_handler(commands=['logout'])
def logout(message):
    if db.if_id_exist(message.chat.id):
        db.delete_field(message.chat.id)
        bot.send_message(message.chat.id, 'Готово.')
    else:
        bot.send_message(message.chat.id, 'Вы уже вышли.')

# Проверка статуса входа (служебная).
@bot.message_handler(commands=['status'])
def status(message):
    if db.if_id_exist(message.chat.id):
        bot.send_message(message.chat.id, 'Вы вошли.')
    else:
        bot.send_message(message.chat.id, 'Вы не вошли.')


bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url=os.getenv("WEBHOOK_URL_BASE") + os.getenv("WEBHOOK_URL_PATH"),
                certificate=open(os.getenv("WEBHOOK_SSL_CERT"), 'r'))

app.run(host=os.getenv("WEBHOOK_LISTEN"),
        port=int(os.getenv("WEBHOOK_PORT")),
        ssl_context=(os.getenv("WEBHOOK_SSL_CERT"),
                     os.getenv("WEBHOOK_SSL_PRIV")),
        debug=True)
