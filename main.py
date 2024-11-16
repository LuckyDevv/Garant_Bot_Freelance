from os import mkdir
from os.path import exists
import telebot
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from ConfigController import ConfigController, ConfigType

TOKEN = '7406106326:AAHwTzdBS_bDqw-gVSr7WzgrePcbhBnklOU'  # Введите сюда токен своего Telegram-бота
bot = telebot.TeleBot(TOKEN)
if not exists('configs'):
    mkdir('configs')
grants_config = ConfigController('configs/grants.json', ConfigType.JSON)
admins_config = ConfigController('configs/admins.json', ConfigType.JSON)
online_config = ConfigController('configs/online.json', ConfigType.JSON)
user_keyboard = InlineKeyboardMarkup()
user_keyboard.add(InlineKeyboardButton("Список гарантов онлайн", callback_data='grant_list'))
grant_keyboard = InlineKeyboardMarkup()
grant_keyboard.add(InlineKeyboardButton("Список гарантов онлайн", callback_data='grant_list'))
grant_keyboard.add(InlineKeyboardButton("Я онлайн", callback_data='im_online'),
             InlineKeyboardButton("Я оффлайн", callback_data='im_offline'))
admins_keyboard = InlineKeyboardMarkup()
admins_keyboard.add(InlineKeyboardButton("Список гарантов онлайн", callback_data='grant_list'),
             InlineKeyboardButton("Список всех гарантов", callback_data='grant_list_all'))
admins_keyboard.add(InlineKeyboardButton("Я онлайн", callback_data='im_online'),
             InlineKeyboardButton("Я оффлайн", callback_data='im_offline'))
owner_username = 'sky4arg'  # sky4arg


@bot.message_handler(commands=['add_grant'])
def add_grant(message):
    username = message.from_user.username
    if username is None:
        username = ''
    if admins_config.exists('@'+username) or admins_config.exists(message.from_user.id) or username == owner_username:
        text = str(message.text).split(' ')
        if len(text) >= 2:
            user = get_user(text[1].strip())
            if not grants_config.exists(user):
                grants_config.set(user, '')
                grants_config.save()
                bot.send_message(message.chat.id, 'Вы успешно добавили гаранта ' + user + ' в список гарантов!',
                                 reply_markup=admins_keyboard)
            else:
                bot.send_message(message.chat.id, 'Этот гарант уже находится в списке гарантов!',
                                 reply_markup=admins_keyboard)
        else:
            bot.send_message(message.chat.id, 'Вы не ввели id/username гаранта!',
                             reply_markup=admins_keyboard)
    else:
        send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)


@bot.message_handler(commands=['remove_grant'])
def remove_grant(message):
    username = message.from_user.username
    if username is None:
        username = ''
    if admins_config.exists('@'+username) or admins_config.exists(message.from_user.id) or username == owner_username:
        text = str(message.text).split(' ')
        if len(text) >= 2:
            user = get_user(text[1].strip())
            if online_config.exists(user):
                online_config.remove(user)
                online_config.save()
            if grants_config.exists(user):
                grants_config.remove(user)
                grants_config.save()
                bot.send_message(message.chat.id, 'Вы успешно удалили гаранта ' + user + ' из списка гарантов!',
                                 reply_markup=admins_keyboard)
            else:
                bot.send_message(message.chat.id, 'Этот гарант не находится в списке гарантов!',
                                 reply_markup=admins_keyboard)
        else:
            bot.send_message(message.chat.id, 'Вы не ввели id/username гаранта!',
                             reply_markup=admins_keyboard)
    else:
        send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)


@bot.message_handler(commands=['add_admin'])
def add_admin(message):
    username = message.from_user.username
    if username is None:
        username = ''
    if username == owner_username:
        text = str(message.text).split(' ')
        if len(text) >= 2:
            user = get_user(text[1].strip())
            if not admins_config.exists(user):
                admins_config.set(user)
                admins_config.save()
                bot.send_message(message.chat.id, 'Вы успешно добавили админа ' + user + ' в список админов!',
                                 reply_markup=admins_keyboard)
            else:
                bot.send_message(message.chat.id, 'Этот админ уже находится в списке админов!',
                                 reply_markup=admins_keyboard)
        else:
            bot.send_message(message.chat.id, 'Вы не ввели id/username админа!',
                             reply_markup=admins_keyboard)
    else:
        send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)


@bot.message_handler(commands=['remove_admin'])
def remove_admin(message):
    username = message.from_user.username
    if username is None:
        username = ''
    if username == owner_username:
        text = str(message.text).split(' ')
        if len(text) >= 2:
            user = get_user(text[1].strip())
            if admins_config.exists(user):
                admins_config.remove(user)
                admins_config.save()
                bot.send_message(message.chat.id, 'Вы успешно удалили админа ' + user + ' из списка админов!', reply_markup=admins_keyboard)
            else:
                bot.send_message(message.chat.id, 'Этот админ не находится в списке админов!', reply_markup=admins_keyboard)
        else:
            bot.send_message(message.chat.id, 'Вы не ввели id/username админа!', reply_markup=admins_keyboard)
    else:
        send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)


@bot.message_handler(commands=['set_prefix'])
def set_prefix(message):
    username = message.from_user.username
    if username is None:
        username = ''
    if username == owner_username or admins_config.exists(message.from_user.id) or admins_config.exists('@'+username):
        text = str(message.text).split(' ')
        if len(text) >= 3:
            user = get_user(text[1].strip())
            prefix = text[2].strip()
            if grants_config.exists(user):
                grants_config.set(user, prefix)
                grants_config.save()
                bot.send_message(message.chat.id, 'Вы успешно установили префикс гаранту ' + user + ' - '+prefix,
                                 reply_markup=admins_keyboard)
            else:
                bot.send_message(message.chat.id, 'Пользователь не является гарантом!', reply_markup=admins_keyboard)
        else:
            bot.send_message(message.chat.id, 'Вы не ввели все параметры! Использование: `/set_prefix` id|username prefix', reply_markup=admins_keyboard)
    else:
        send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)


@bot.message_handler(content_types=['text'])
def start_command(message):
    userid = message.from_user.id
    username = message.from_user.username
    if username is None:
        username = ''
    if admins_config.exists(userid) or admins_config.exists('@'+username) or username == owner_username:
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=admins_keyboard)
    elif grants_config.exists(userid) or grants_config.exists('@'+username):
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=grant_keyboard)
    else:
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=user_keyboard)


@bot.callback_query_handler(func=lambda call: call.data)
def query_handler_assortment(call):
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    if call.data == 'grant_list':
        grant_list = online_config.get_all(False)
        if len(grant_list) == 0:
            send_keyboard(grant_keyboard, call.message.message_id, call.message.chat.id, 'Сейчас нет гарантов в онлайне!')
            return
        grant_result = 'Список гарантов онлайн:\n\n'
        for grant in grant_list:
            grant = str(grant)
            try:
                grant = str(int(grant))
                if grants_config.exists(grant):
                    prefix = grants_config.get(grant)
                    if prefix != True and prefix != '' and prefix != False:
                        grant_result += 'tg://user?id=' + grant + ' | ' + prefix +'\n'
                    else:
                        grant_result += 'tg://user?id=' + grant + '\n'
            except ValueError:
                if grant.startswith('@'):
                    if grants_config.exists(grant):
                        prefix = grants_config.get(grant)
                        if prefix != True and prefix != '' and prefix != False:
                            grant_result += grant + ' | ' + prefix +'\n'
                        else:
                            grant_result += grant + '\n'
                else:
                    if grants_config.exists('@'+grant):
                        prefix = grants_config.get('@'+grant)
                        if prefix != True and prefix != '' and prefix != False:
                            grant_result += '@' + grant + ' | ' + prefix +'\n'
                        else:
                            grant_result += '@' + grant + '\n'
        userid = call.from_user.id
        username = call.from_user.username
        if username is None:
            username = ''
        if admins_config.exists(userid) or admins_config.exists('@' + username) or username == owner_username:
            send_keyboard(admins_keyboard, call.message.message_id, call.message.chat.id, grant_result)
        elif grants_config.exists(userid) or grants_config.exists('@' + username):
            send_keyboard(grant_keyboard, call.message.message_id, call.message.chat.id, grant_result)
        else:
            send_keyboard(user_keyboard, call.message.message_id, call.message.chat.id, grant_result)
    elif call.data == 'grant_list_all':
        username = call.from_user.username
        if username is None:
            username = ''
        userid = call.from_user.id
        if admins_config.exists(userid) or admins_config.exists('@' + username) or username == owner_username:
            grant_list = grants_config.get_all()
            if len(grant_list) == 0:
                send_keyboard(grant_keyboard, call.message.message_id, call.message.chat.id,
                              'На данный момент не добавлено ни одного гаранта!')
                return
            grant_result = 'Список гарантов:\n\n'
            for grant, prefix in grant_list.items():
                grant = str(grant)
                try:
                    grant = str(int(grant))
                    if prefix != True and prefix != '' and prefix != False:
                        grant_result += 'tg://user?id=' + grant + ' | ' + prefix + '\n'
                    else:
                        grant_result += 'tg://user?id=' + grant + '\n'
                except ValueError:
                    if grant.startswith('@'):
                        if prefix != True and prefix != '' and prefix != False:
                            grant_result += grant + ' | ' + prefix +  '\n'
                        else:
                            grant_result += grant + '\n'
                    else:
                        if prefix != True and prefix != '' and prefix != False:
                            grant_result += '@' + grant + ' | ' + prefix +  '\n'
                        else:
                            grant_result += '@' + grant + '\n'
            send_keyboard(admins_keyboard, call.message.message_id, call.message.chat.id, grant_result)
        else:
            send_no_access(call.message.chat.id, call.message.message_id, username, userid)
    elif call.data == 'im_online':
        username = call.from_user.username
        if username is None:
            username = ''
        userid = call.from_user.id
        if admins_config.exists(userid) or admins_config.exists('@' + username) or username == owner_username:
            kb = admins_keyboard
        else:
            kb = grant_keyboard
        if online_config.exists('@'+username) or online_config.exists(userid):
            send_keyboard(kb, call.message.message_id, call.message.chat.id, 'Вы уже онлайн!')
            return
        if (grants_config.exists(userid) or (username != '' and grants_config.exists('@'+username))) or (admins_config.exists(userid) or (username != '' and admins_config.exists('@'+username)) or username == owner_username):
            if username != '':
                online_config.set('@'+username)
            else:
                online_config.set(userid)
            online_config.save()
            send_keyboard(kb, call.message.message_id, call.message.chat.id, 'Вы успешно включили онлайн!')
        else:
            send_keyboard(user_keyboard, call.message.message_id, call.message.chat.id, 'У вас нет доступа к этой команде!')
    elif call.data == 'im_offline':
        username = call.from_user.username
        if username is None:
            username = ''
        userid = call.from_user.id
        if (grants_config.exists(userid) or (username != '' and grants_config.exists('@'+username))) or (admins_config.exists(userid) or (username != '' and admins_config.exists('@'+username)) or username == owner_username):
            if admins_config.exists(userid) or admins_config.exists('@'+username) or username == owner_username:
                kb = admins_keyboard
            else:
                kb = grant_keyboard
            if online_config.exists(userid):
                online_config.remove(userid)
            elif username != '' and online_config.exists('@'+username):
                online_config.remove('@'+username)
            else:
                send_keyboard(kb, call.message.message_id, call.message.chat.id, 'Вы не онлайн!')
                return
            online_config.save()
            send_keyboard(kb, call.message.message_id, call.message.chat.id, 'Вы успешно выключили онлайн!')
        else:
            send_keyboard(user_keyboard, call.message.message_id, call.message.chat.id, 'У вас нет доступа к этой команде!')


def send_keyboard(keyboard, message_id, chat_id, text):
    try:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=keyboard)
    except ApiTelegramException as e:
        if e.error_code != 400:
            bot.send_message(chat_id, text, reply_markup=keyboard)


def get_user(attr):
    try:
        attr = int(attr)
    except ValueError:
        if not attr.startswith('@'):
            attr = '@' + attr
    return attr


def send_no_access(chat_id, message_id, username, userid, keyboard=True):
    if keyboard:
        if grants_config.exists(userid) or grants_config.exists('@' + username):
            send_keyboard(grant_keyboard, message_id, chat_id,
                          'У вас нет доступа к этой команде!')
        else:
            send_keyboard(user_keyboard, message_id, chat_id,
                          'У вас нет доступа к этой команде!')
    else:
        if grants_config.exists(userid) or grants_config.exists('@' + username):
            bot.send_message(chat_id, 'У вас нет доступа к этой команде!', reply_markup=grant_keyboard)
        else:
            bot.send_message(chat_id, 'У вас нет доступа к этой команде!', reply_markup=user_keyboard)


bot.polling()