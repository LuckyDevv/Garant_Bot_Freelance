from telebot.apihelper import ApiTelegramException

import DatabaseManager


class CommandHandler:
    def __init__(self, bot, manager_db, user_kb, grant_kb, admin_kb):
        self.bot = bot
        self.manager_db = manager_db
        self.keyboards = [
            user_kb,
            grant_kb,
            admin_kb
        ]

    def add_broker(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(' ')
            if len(text) >= 2:
                user = text[1].strip()
                result = self.manager_db.set_broker(user, True)
                if result[0] == "yes":
                    self.bot.send_message(message.chat.id, 'Вы успешно добавили гаранта ' + self.manager_db.get_user_tgname(user) + ' в список гарантов!',
                                     reply_markup=self.keyboards[2])
                    try:
                        print(result[1])
                        self.bot.send_message(result[1], 'Вас назначили от должности гаранта!', reply_markup=self.keyboards[1])
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                else:
                    self.bot.send_message(message.chat.id, 'Этот гарант уже находится в списке гарантов!',
                                     reply_markup=self.keyboards[2])
            else:
                self.bot.send_message(message.chat.id, 'Вы не ввели все параметры! Использование: `/add_broker [id|@]`',
                                 reply_markup=self.keyboards[2], parse_mode='Markdown')
        else:
            self.send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)

    def remove_broker(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(' ')
            if len(text) >= 2:
                user = text[1].strip()
                result = self.manager_db.set_broker(user, False)
                if result[0] == "yes":
                    self.bot.send_message(message.chat.id, 'Вы успешно удалили гаранта ' + self.manager_db.get_user_tgname(user) + ' из списка гарантов!',
                                     reply_markup=self.keyboards[2])
                    try:
                        print(result[1])
                        self.bot.send_message(result[1], 'Вас отстранили от должности гаранта!', reply_markup=self.keyboards[0])
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                else:
                    self.bot.send_message(message.chat.id, 'Этот гарант не находится в списке гарантов!',
                                     reply_markup=self.keyboards[2])
            else:
                self.bot.send_message(message.chat.id, 'Вы не ввели все параметры! Использование: `/remove_broker [id|@]`',
                                 reply_markup=self.keyboards[2], parse_mode='Markdown')
        else:
            self.send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)

    def add_admin(self, message):
        username = message.from_user.username
        if self.manager_db.is_owner(username):
            text = str(message.text).split(' ')
            if len(text) >= 2:
                user = text[1].strip()
                result = self.manager_db.set_admin(user, True)
                if result[0] == "yes":
                    self.bot.send_message(message.chat.id, 'Вы успешно добавили админа ' + self.manager_db.get_user_tgname(user) + ' в список админов!',
                                     reply_markup=self.keyboards[2])
                    try:
                        self.bot.send_message(result[1], 'Вас назначили от должности админа!', reply_markup=self.keyboards[2])
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                else:
                    self.bot.send_message(message.chat.id, 'Этот админ уже находится в списке админов!',
                                     reply_markup=self.keyboards[2])
            else:
                self.bot.send_message(message.chat.id, 'Вы не ввели все параметры! Использование: `/add_admin [id|@]`',
                                 reply_markup=self.keyboards[2], parse_mode='Markdown')
        else:
            self.send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)

    def remove_admin(self, message):
        username = message.from_user.username
        if username is None:
            username = ''
        if self.manager_db.is_owner(username):
            text = str(message.text).split(' ')
            if len(text) >= 2:
                user = text[1].strip()
                result = self.manager_db.set_admin(user, False)
                if result[0] == "yes":
                    self.bot.send_message(message.chat.id, 'Вы успешно удалили админа ' + self.manager_db.get_user_tgname(user) + ' из списка админов!',
                                     reply_markup=self.keyboards[2])
                    try:
                        self.bot.send_message(result[1], 'Вас отстранили от должности админа!', reply_markup=self.keyboards[0])
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                else:
                    self.bot.send_message(message.chat.id, 'Этот админ не находится в списке админов!',
                                     reply_markup=self.keyboards[2])
            else:
                self.bot.send_message(message.chat.id, 'Вы не ввели все параметры! Использование: `/remove_admin [id|@]`',
                                 reply_markup=self.keyboards[2], parse_mode='Markdown')
        else:
            self.send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)

    def set_prefix(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(' ')
            if len(text) >= 3:
                user = text[1].strip()
                prefix = text[2].strip()
                if self.manager_db.set_prefix_broker(user, prefix):
                    self.bot.send_message(message.chat.id, 'Вы успешно установили префикс гаранту ' + self.manager_db.get_user_tgname(user) + ' - ' + prefix,
                                     reply_markup=self.keyboards[2])
                else:
                    self.bot.send_message(message.chat.id, 'Пользователь не является гарантом!',
                                     reply_markup=self.keyboards[2])
            else:
                self.bot.send_message(message.chat.id,
                                 'Вы не ввели все параметры! Использование: `/set_prefix [id|@] [prefix]`',
                                 reply_markup=self.keyboards[2], parse_mode='Markdown')
        else:
            self.send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)

    def ban_user(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(' ')
            if len(text) >= 3:
                user = text[1].strip()
                if user == username or user == userid or user == f'@{username}':
                    self.bot.send_message(message.chat.id, f'Нельзя заблокировать самого себя!',
                                     reply_markup=self.keyboards[2])
                    return
                reason = ' '.join(text[2:]).strip()
                result = self.manager_db.ban_user(user, reason)
                if result[0] == "yes":
                    self.bot.send_message(message.chat.id,
                                     f'Вы успешно заблокировали пользователя {self.manager_db.get_user_tgname(user)} по причине "{reason}"!',
                                     reply_markup=self.keyboards[2])
                    try:
                        if type(username) != str:
                            username_2 = f'tg://user?id={userid}'
                        else:
                            username_2 = f'@{username}'
                        self.bot.send_message(result[1], f"Вы были заблокированы администратором {username_2}! Причина: {reason}")
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                else:
                    self.bot.send_message(message.chat.id, f"Пользователь {username} уже находится в блокировке!",
                                     reply_markup=self.keyboards[2])
            else:
                self.bot.send_message(message.chat.id, 'Вы не ввели все параметры! Использование: `/ban [id|@] [причина]`',
                                 reply_markup=self.keyboards[2], parse_mode='Markdown')
        else:
            self.send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)

    def unban_user(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(' ')
            if len(text) >= 2:
                user = text[1].strip()
                result = self.manager_db.unban_user(user)
                if result[0] == "yes":
                    self.bot.send_message(message.chat.id,
                                          f'Вы успешно разблокировали пользователя {self.manager_db.get_user_tgname(user)}!',
                                          reply_markup=self.keyboards[2])
                    try:
                        if type(username) != str:
                            username_2 = f'tg://user?id={userid}'
                        else:
                            username_2 = f'@{username}'
                        self.bot.send_message(result[1], f"Вы были разблокированы администратором {username_2}!")
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                else:
                    self.bot.send_message(message.chat.id, f"Пользователь {user} не находится в блокировке!",
                                          reply_markup=self.keyboards[2])
            else:
                self.bot.send_message(message.chat.id,
                                      'Вы не ввели все параметры! Использование: `/unban [id|@]`',
                                      reply_markup=self.keyboards[2], parse_mode='Markdown')
        else:
            self.send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)

    def warn_user(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(' ')
            if len(text) >= 3:
                user = text[1].strip()
                if user == username or user == userid or user == f'@{username}':
                    self.bot.send_message(message.chat.id, f'Нельзя выдать предупреждение самому себе!',
                                     reply_markup=self.keyboards[2])
                    return
                reason = ' '.join(text[2:]).strip()
                result = self.manager_db.warn_user(user, reason)
                if result[0] == "banned":
                    self.bot.send_message(message.chat.id, "Данный пользователь уже заблокирован!",
                                     reply_markup=self.keyboards[2])
                    return
                text_send = f'Вы успешно выдали предупреждение ({result[1]}/3) пользователю {self.manager_db.get_user_tgname(user)} по причине "{reason}"!'
                if result[0] == "ban":
                    text_send += '\n\nИз-за того, что пользователь набрал 3/3 предупреждений, он был заблокирован!'
                if result[2] != 0:
                    if type(username) != str:
                        username_2 = f'tg://user?id={userid}'
                    else:
                        username_2 = f'@{username}'
                    text_send_user = f'Вы получили предупреждение ({result[1]}/3) от администратора {username_2}! Причина: "{reason}".'
                    if result[0] == "warn":
                        text_send_user += "\n\nЕсли вы наберете 3/3 предупреждений, то будете заблокированы в боте!"
                    elif result[0] == "ban":
                        text_send_user += "\n\nПоскольку вы набрали 3/3 предупреждений, вы были заблокированы в боте!"
                    try:
                        self.bot.send_message(result[2], text_send_user, parse_mode='Markdown')
                        text_send += '\n\nУведомление успешно отправлено пользователю.'
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                        text_send += '\n\nК сожалению, не удалось отправить уведомление пользователю, поскольку он заблокировал бота.'
                else:
                    text_send += '\n\nК сожалению, не удалось отправить уведомление пользователю, поскольку он никогда не писал боту.'
                self.bot.send_message(message.chat.id, text_send, reply_markup=self.keyboards[2])
            else:
                self.bot.send_message(message.chat.id, 'Вы не ввели все параметры! Использование: `/warn [id|@] [причина]`',
                                 reply_markup=self.keyboards[2], parse_mode='Markdown')
        else:
            self.send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)

    def unwarn_user(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(' ')
            if len(text) >= 2:
                user = text[1].strip()
                result = self.manager_db.unwarn_user(user)
                if result[0] == "banned":
                    self.bot.send_message(message.chat.id, 'Невозможно снять предупреждение, поскольку пользователь заблокирован!', reply_markup=self.keyboards[2])
                elif result[0] == "yes":
                    self.bot.send_message(message.chat.id, f'Предупреждение с пользователя {self.manager_db.get_user_tgname(user)} успешно снято! Теперь у него {result[2]}/3 предупреждений!', reply_markup=self.keyboards[2])
                    try:
                        if type(username) != str:
                            username_2 = f'tg://user?id={userid}'
                        else:
                            username_2 = f'@{username}'
                        self.bot.send_message(result[1], f'Администратор {username_2} снял с ваc предупреждение! Теперь у вас {result[2]}/3 предупреждений!')
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                elif result[0] == "no":
                    self.bot.send_message(message.chat.id, 'У пользователя нет активных предупреждений!', reply_markup=self.keyboards[2])
            else:
                self.bot.send_message(message.chat.id,
                                      'Вы не ввели все параметры! Использование: `/unwarn [id|@]`',
                                      reply_markup=self.keyboards[2], parse_mode='Markdown')
        else:
            self.send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)

    def mail_send(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        username_2 = self.manager_db.get_normal_name(username)
        userid_2 = self.manager_db.get_normal_id(userid)
        if username_2 == '':
            username_2 = f"tg://user?id={userid_2}"
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(' ')
            if len(text) >= 2:
                text = ' '.join(text[1:]).strip()
                chat_ids = self.manager_db.get_all_chat_id_brokers()
                length = len(chat_ids)
                if length > 0:
                    count = 0
                    for chat_id in chat_ids:
                        if chat_id == message.chat.id:
                            length -= 1
                            continue
                        try:
                            self.bot.send_message(chat_id, text + f"\n\nАвтор рассылки: {username_2}", parse_mode='Markdown')
                            count += 1
                        except ApiTelegramException as e:
                            DatabaseManager.create_log(e)
                    if count == 0:
                        text_send = 'Не удалось отправить сообщение ни одному гаранту!'
                    else:
                        text_send = f'Сообщение успешно разослано в {count}/{length} чатов!'
                    self.bot.send_message(message.chat.id, text_send, reply_markup=self.keyboards[2])
                else:
                    self.bot.send_message(message.chat.id,
                                     'Список пользователей, которым может быть разослано сообщение, пуст!',
                                     reply_markup=self.keyboards[2])
            else:
                self.bot.send_message(message.chat.id, 'Вы не ввели все параметры! Использование: `/mail [текст]`',
                                 reply_markup=self.keyboards[2])
        else:
            self.send_no_access(message.chat.id, message.message_id, username, message.from_user.id, False)

    def handle_text(self, message):
        userid = message.from_user.id
        username = message.from_user.username
        if self.manager_db.is_banned(userid, username):
            return
        self.manager_db.log_user(userid, username, message.chat.id)
        if self.manager_db.is_admin(userid, username):
            self.bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=self.keyboards[2])
        elif self.manager_db.is_broker(userid, username):
            self.bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=self.keyboards[1])
        else:
            self.bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=self.keyboards[0])

    def send_keyboard(self, keyboard, message_id, chat_id, text):
        try:
            self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=keyboard)
        except ApiTelegramException as e:
            DatabaseManager.create_log(e)
            if e.error_code != 400:
                self.bot.send_message(chat_id, text, reply_markup=keyboard)

    def send_no_access(self, chat_id, message_id, username, userid, keyboard=True):
        if keyboard:
            if self.manager_db.is_broker(userid, username):
                self.send_keyboard(self.keyboards[1], message_id, chat_id, 'У вас нет доступа к этой команде!')
            else:
                self.send_keyboard(self.keyboards[0], message_id, chat_id, 'У вас нет доступа к этой команде!')
        else:
            if self.manager_db.is_broker(userid, username):
                self.bot.send_message(chat_id, 'У вас нет доступа к этой команде!', reply_markup=self.keyboards[1])
            else:
                self.bot.send_message(chat_id, 'У вас нет доступа к этой команде!', reply_markup=self.keyboards[0])