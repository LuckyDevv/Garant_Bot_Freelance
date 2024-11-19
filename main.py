from time import strftime, gmtime
import telebot
from CommandHandler import CommandHandler
from DatabaseManager import DatabaseManager
import Initializer
from QueryHandler import QueryHandler
import atexit


TOKEN = "7579498106:AAGbTmMeeP9JrbWTMUFIr8a6kDl9xmprQDo"  # Введите сюда токен своего Telegram-бота
bot = telebot.TeleBot(TOKEN)
bot.set_webhook()
Initializer.create_dirs()


def msg_log(message):
    print(message)
    with open("/home/luckydevv/broker_bot/Work.log", "a") as myfile:
        myfile.write(message)
        myfile.close()
        try:
            bot.send_message(1199296238, message)
        except:
            pass


atexit.register(
    msg_log,
    "Скрипт завершил свою работу в " + strftime("%d.%m.%Y %H:%M:%S", gmtime()),
)
msg_log("Скрипт запущен в " + strftime("%d.%m.%Y %H:%M:%S", gmtime()))

user_keyboard = Initializer.get_keyboard("user")
broker_keyboard = Initializer.get_keyboard("broker")
admin_keyboard = Initializer.get_keyboard("admin")

database_manager = DatabaseManager()
command_handler = CommandHandler(
    bot, database_manager, user_keyboard, broker_keyboard, admin_keyboard
)
query_handler = QueryHandler(
    bot, database_manager, user_keyboard, broker_keyboard, admin_keyboard
)

commands = {
    "/add_broker": command_handler.add_broker,
    "/remove_broker": command_handler.remove_broker,
    "/add_admin": command_handler.add_admin,
    "/remove_admin": command_handler.remove_admin,
    "/set_prefix": command_handler.set_prefix,
    "/ban": command_handler.ban_user,
    "/warn": command_handler.warn_user,
    "/mail": command_handler.mail_send,
    "/unban": command_handler.unban_user,
    "/unwarn": command_handler.unwarn_user,
}

queries = {
    "broker_online_list": query_handler.broker_online_list,
    "broker_all_list": query_handler.broker_all_list,
    "broker_online": query_handler.broker_online,
    "broker_offline": query_handler.broker_offline,
    "admin_online_list": query_handler.admin_online_list,
    "admin_all_list": query_handler.admin_all_list,
    "admin_online": query_handler.admin_online,
    "admin_offline": query_handler.admin_offline,
}


@bot.message_handler(content_types=["text"])
def t1(message):
    command = message.text.split()[0]
    if command in commands:
        commands[command](message)
    else:
        command_handler.handle_text(message)


@bot.callback_query_handler(func=lambda call: call.data)
def q1(call):
    userid = call.from_user.id
    username = call.from_user.username
    if database_manager.is_banned(userid, username):
        banned = True
    else:
        banned = False
    try:
        if banned:
            bot.answer_callback_query(call.id, "Вы заблокированы!")
            return
    except:
        if banned:
            return
    if call.data in queries:
        queries[call.data](call, userid, username)


bot.polling()
