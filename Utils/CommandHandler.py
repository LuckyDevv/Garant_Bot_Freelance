from telebot import types
from telebot.apihelper import ApiTelegramException

from Utils import DatabaseManager


class CommandHandler:
    def __init__(self, bot, manager_db, user_kb, grant_kb, admin_kb, ab_kb):
        self.bot = bot
        self.manager_db = manager_db
        self.keyboards = [user_kb, grant_kb, admin_kb, ab_kb]

    def add_broker(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(" ")
            if len(text) >= 2:
                user = text[1].strip()
                result = self.manager_db.set_broker(user, True)
                if result[0] == "yes":
                    self.bot.send_message(
                        message.chat.id,
                        "Вы успешно добавили гаранта "
                        + self.manager_db.get_user_tgname(user)
                        + " в список гарантов!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
                    try:
                        self.bot.send_message(
                            result[1],
                            "Вас назначили на должность гаранта!\n\n"
                            "Вот ссылка-приглашение в чат гарантов: https://t.me/+VfNF4q0ptG0xMWM1",
                            reply_markup=self.keyboards[1],
                            disable_web_page_preview=True
                        )
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                else:
                    self.bot.send_message(
                        message.chat.id,
                        "Этот гарант уже находится в списке гарантов!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
            else:
                self.bot.send_message(
                    message.chat.id,
                    "Вы не ввели все параметры! Использование: `/+гарант [id|@]`",
                    reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    parse_mode="Markdown",
                )
        else:
            self.send_no_access(
                message.chat.id,
                message.message_id,
                username,
                message.from_user.id,
                False,
            )

    def remove_broker(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(" ")
            if len(text) >= 2:
                user = text[1].strip()
                result = self.manager_db.set_broker(user, False)
                if result[0] == "yes":
                    self.bot.send_message(
                        message.chat.id,
                        "Вы успешно удалили гаранта "
                        + self.manager_db.get_user_tgname(user)
                        + " из списка гарантов!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
                    try:
                        self.bot.send_message(
                            result[1],
                            "Вас отстранили от должности гаранта!",
                            reply_markup=self.keyboards[0],
                        )
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                else:
                    self.bot.send_message(
                        message.chat.id,
                        "Этот гарант не находится в списке гарантов!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
            else:
                self.bot.send_message(
                    message.chat.id,
                    "Вы не ввели все параметры! Использование: `/-гарант [id|@]`",
                    reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    parse_mode="Markdown",
                )
        else:
            self.send_no_access(
                message.chat.id,
                message.message_id,
                username,
                message.from_user.id,
                False,
            )

    def add_admin(self, message):
        username = message.from_user.username
        if self.manager_db.is_owner(username):
            text = str(message.text).split(" ")
            if len(text) >= 2:
                user = text[1].strip()
                result = self.manager_db.set_admin(user, True)
                if result[0] == "yes":
                    self.bot.send_message(
                        message.chat.id,
                        "Вы успешно добавили администратора "
                        + self.manager_db.get_user_tgname(user)
                        + " в список администраторов!",
                        reply_markup=self.keyboards[3],
                    )
                    try:
                        self.bot.send_message(
                            result[1],
                            "Вас назначили на должность администратора!",
                            reply_markup=self.keyboards[2] if self.manager_db.is_broker(username, username) else self.keyboards[3],
                        )
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                else:
                    self.bot.send_message(
                        message.chat.id,
                        "Этот администратор уже находится в списке администраторов!",
                        reply_markup=self.keyboards[3],
                    )
            else:
                self.bot.send_message(
                    message.chat.id,
                    "Вы не ввели все параметры! Использование: `/+адм [id|@]`",
                    reply_markup=self.keyboards[3],
                    parse_mode="Markdown",
                )
        else:
            self.send_no_access(
                message.chat.id,
                message.message_id,
                username,
                message.from_user.id,
                False,
            )

    def remove_admin(self, message):
        username = message.from_user.username
        if username is None:
            username = ""
        if self.manager_db.is_owner(username):
            text = str(message.text).split(" ")
            if len(text) >= 2:
                user = text[1].strip()
                result = self.manager_db.set_admin(user, False)
                if result[0] == "yes":
                    self.bot.send_message(
                        message.chat.id,
                        "Вы успешно удалили администратора "
                        + self.manager_db.get_user_tgname(user)
                        + " из списка администраторов!",
                        reply_markup=self.keyboards[3],
                    )
                    try:
                        self.bot.send_message(
                            result[1],
                            "Вас отстранили от должности администратора!",
                            reply_markup=self.keyboards[1] if self.manager_db.is_broker(username, username) else self.keyboards[0],
                        )
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                else:
                    self.bot.send_message(
                        message.chat.id,
                        "Этот администратор не находится в списке администраторов!",
                        reply_markup=self.keyboards[3],
                    )
            else:
                self.bot.send_message(
                    message.chat.id,
                    "Вы не ввели все параметры! Использование: `/-адм [id|@]`",
                    reply_markup=self.keyboards[3],
                    parse_mode="Markdown",
                )
        else:
            self.send_no_access(
                message.chat.id,
                message.message_id,
                username,
                message.from_user.id,
                False,
            )

    def set_prefix(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(" ")
            if len(text) >= 4:
                prefix_type = text[1].strip()
                user = text[2].strip()
                prefix = text[3].strip()
                if prefix_type == "0":
                    if self.manager_db.set_prefix_broker(user, prefix):
                        self.bot.send_message(
                            message.chat.id,
                            "Вы успешно установили префикс для гаранта "
                            + self.manager_db.get_user_tgname(user)
                            + " - "
                            + prefix,
                            reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                        )
                    else:
                        self.bot.send_message(
                            message.chat.id,
                            "Пользователь не является гарантом!",
                            reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                        )
                elif prefix_type == "1":
                    if not self.manager_db.is_owner(username):
                        self.bot.send_message(
                            message.chat.id,
                            "У вас недостаточно прав!",
                            reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                        )
                        return
                    if self.manager_db.set_prefix_admin(user, prefix):
                        self.bot.send_message(
                            message.chat.id,
                            "Вы успешно установили префикс для администратора "
                            + self.manager_db.get_user_tgname(user)
                            + " - "
                            + prefix,
                            reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                        )
                    else:
                        self.bot.send_message(
                            message.chat.id,
                            "Пользователь не является администратором!",
                            reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                        )
                else:
                    self.bot.send_message(
                        message.chat.id,
                        "Неизвестный тип операции!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
            else:
                self.bot.send_message(
                    message.chat.id,
                    "Вы не ввели все параметры! Использование: `/преф [0|1] [id|@] [prefix]`, где 0 - префикс для гарантов, а 1 - для администраторов",
                    reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    parse_mode="Markdown",
                )
        else:
            self.send_no_access(
                message.chat.id,
                message.message_id,
                username,
                message.from_user.id,
                False,
            )

    def ban_user(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(" ")
            if len(text) >= 3:
                user = text[1].strip()
                if user == username or user == userid or user == f"@{username}":
                    self.bot.send_message(
                        message.chat.id,
                        f"Нельзя заблокировать самого себя!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
                    return
                reason = " ".join(text[2:]).strip()
                result = self.manager_db.ban_user(user, reason)
                if result[0] == "yes":
                    self.bot.send_message(
                        message.chat.id,
                        f'Вы успешно заблокировали пользователя {self.manager_db.get_user_tgname(user)} по причине "{reason}"!',
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
                    self.send_log(
                        f"заблокировал пользователя {self.manager_db.get_user_tgname(user)}",
                        username,
                        userid
                    )
                    try:
                        if type(username) != str:
                            username_2 = f"tg://user?id={userid}"
                        else:
                            username_2 = f"@{username}"
                        self.bot.send_message(
                            result[1],
                            f"Вы были заблокированы администратором {username_2}! Причина: {reason}",
                        )
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                else:
                    self.bot.send_message(
                        message.chat.id,
                        f"Пользователь {username} уже находится в блокировке!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
            else:
                self.bot.send_message(
                    message.chat.id,
                    "Вы не ввели все параметры! Использование: `/бан [id|@] [причина]`",
                    reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    parse_mode="Markdown",
                )
        else:
            self.send_no_access(
                message.chat.id,
                message.message_id,
                username,
                message.from_user.id,
                False,
            )

    def unban_user(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(" ")
            if len(text) >= 2:
                user = text[1].strip()
                result = self.manager_db.unban_user(user)
                if result[0] == "yes":
                    self.bot.send_message(
                        message.chat.id,
                        f"Вы успешно разблокировали пользователя {self.manager_db.get_user_tgname(user)}!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
                    self.send_log(
                        f"разблокировал пользователя {self.manager_db.get_user_tgname(user)}",
                        username,
                        userid
                    )
                    try:
                        if type(username) != str:
                            username_2 = f"tg://user?id={userid}"
                        else:
                            username_2 = f"@{username}"
                        self.bot.send_message(
                            result[1],
                            f"Вы были разблокированы администратором {username_2}!",
                        )
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                else:
                    self.bot.send_message(
                        message.chat.id,
                        f"Пользователь {user} не находится в блокировке!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
            else:
                self.bot.send_message(
                    message.chat.id,
                    "Вы не ввели все параметры! Использование: `/рбан [id|@]`",
                    reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    parse_mode="Markdown",
                )
        else:
            self.send_no_access(
                message.chat.id,
                message.message_id,
                username,
                message.from_user.id,
                False,
            )

    def warn_user(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(" ")
            if len(text) >= 3:
                user = text[1].strip()
                if user == username or user == userid or user == f"@{username}":
                    self.bot.send_message(
                        message.chat.id,
                        f"Нельзя выдать предупреждение самому себе!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
                    return
                reason = " ".join(text[2:]).strip()
                result = self.manager_db.warn_user(user, reason)
                if result[0] == "banned":
                    self.bot.send_message(
                        message.chat.id,
                        "Данный пользователь уже заблокирован!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
                    return
                text_send = f'Вы успешно выдали предупреждение ({result[1]} из 3) пользователю {self.manager_db.get_user_tgname(user)} по причине "{reason}"!'
                if result[0] == "ban":
                    text_send += "\n\nИз-за того, что пользователь получил 3 из 3 предупреждений, он был заблокирован!"
                if result[2] != 0:
                    if type(username) != str:
                        username_2 = f"tg://user?id={userid}"
                    else:
                        username_2 = f"@{username}"
                    text_send_user = f'Вы получили предупреждение ({result[1]} из 3) от администратора {username_2}! Причина: "{reason}".'
                    if result[0] == "warn":
                        text_send_user += "\n\nЕсли вы получите 3 из 3 предупреждений, то будете заблокированы в боте!"
                    elif result[0] == "ban":
                        text_send_user += "\n\nПоскольку вы получили 3 из 3 предупреждений, вы были заблокированы в боте!"
                    self.send_log(
                        f"выдал предупреждение пользователю {self.manager_db.get_user_tgname(user)}",
                        username,
                        userid
                    )
                    try:
                        self.bot.send_message(
                            result[2], text_send_user, parse_mode="Markdown"
                        )
                        text_send += (
                            "\n\nУведомление успешно отправлено пользователю."
                        )
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                        text_send += "\n\nК сожалению, не удалось отправить уведомление пользователю, так как он заблокировал бота."
                else:
                    text_send += "\n\nК сожалению, не удалось отправить уведомление пользователю, так как он никогда не обращался к боту."
                self.bot.send_message(
                    message.chat.id, text_send, reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2]
                )
            else:
                self.bot.send_message(
                    message.chat.id,
                    "Вы не ввели все параметры! Использование: `/варн [id|@] [причина]`",
                    reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    parse_mode="Markdown",
                )
        else:
            self.send_no_access(
                message.chat.id,
                message.message_id,
                username,
                message.from_user.id,
                False,
            )

    def unwarn_user(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(" ")
            if len(text) >= 2:
                user = text[1].strip()
                result = self.manager_db.unwarn_user(user)
                if result[0] == "banned":
                    self.bot.send_message(
                        message.chat.id,
                        "Невозможно снять предупреждение, так как пользователь заблокирован!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
                elif result[0] == "yes":
                    self.bot.send_message(
                        message.chat.id,
                        f"Предупреждение с пользователя {self.manager_db.get_user_tgname(user)} успешно снято! Теперь у него {result[2]}/3 предупреждений!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
                    self.send_log(
                        f"снял предупреждение с пользователя {self.manager_db.get_user_tgname(user)}",
                        username,
                        userid
                    )
                    try:
                        if type(username) != str:
                            username_2 = f"tg://user?id={userid}"
                        else:
                            username_2 = f"@{username}"
                        self.bot.send_message(
                            result[1],
                            f"Администратор {username_2} снял с ваc предупреждение! Теперь у вас {result[2]}/3 предупреждений!",
                        )
                    except ApiTelegramException as e:
                        DatabaseManager.create_log(e)
                elif result[0] == "no":
                    self.bot.send_message(
                        message.chat.id,
                        "У пользователя нет активных предупреждений!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
            else:
                self.bot.send_message(
                    message.chat.id,
                    "Вы не ввели все параметры! Использование: `/рварн [id|@]`",
                    reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    parse_mode="Markdown",
                )
        else:
            self.send_no_access(
                message.chat.id,
                message.message_id,
                username,
                message.from_user.id,
                False,
            )

    def mail_send(self, message):
        username = message.from_user.username
        userid = message.from_user.id
        if self.manager_db.is_banned(userid, username):
            return
        username_2 = self.manager_db.get_normal_name(username)
        userid_2 = self.manager_db.get_normal_id(userid)
        if username_2 == "":
            username_2 = f"tg://user?id={userid_2}"
        if self.manager_db.is_admin(userid, username):
            text = str(message.text).split(" ")
            if len(text) >= 3:
                argument = text[1]
                if argument == '0':
                    chat_ids = self.manager_db.get_all_chat_id_brokers()
                elif argument == '1':
                    chat_ids = self.manager_db.get_all_chat_id_users()
                else:
                    self.bot.send_message(
                        userid,
                        "Вы ввели неверный агрумент рассылки! Используйте `/mail [0|1] [текст]`,"
                        "где 0 - рассылка гарантов, а 1 - всем пользователям бота"
                    )
                    return
                text = " ".join(text[2:]).strip()
                length = len(chat_ids)
                if length > 0:
                    count = 0
                    for chat_id in chat_ids:
                        if chat_id == message.chat.id:
                            length -= 1
                            continue
                        try:
                            self.bot.send_message(
                                chat_id,
                                text + f"\n\nАвтор рассылки: {username_2}",
                                parse_mode="Markdown",
                            )
                            count += 1
                        except ApiTelegramException as e:
                            DatabaseManager.create_log(e)
                    if count == 0:
                        text_send = (
                            "Не удалось отправить сообщение ни одному пользователю!"
                        )
                    else:
                        text_send = f"Сообщение успешно разослано в {count}/{length} чатов!"
                    self.bot.send_message(
                        message.chat.id,
                        text_send,
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
                else:
                    self.bot.send_message(
                        message.chat.id,
                        "Список пользователей, которым можно разослать сообщение, пуст!",
                        reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    )
            else:
                self.bot.send_message(
                    message.chat.id,
                    "Вы не ввели все параметры! Использование: `/mail [0|1] [текст]`,"
                    " где 0 - рассылка гарантам, а 1 - пользователям чата",
                    reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    parse_mode="Markdown",
                )
        else:
            self.send_no_access(
                message.chat.id,
                message.message_id,
                username,
                message.from_user.id,
                False,
            )

    def set_link(self, message):
        userid = message.from_user.id
        username = message.from_user.username
        if self.manager_db.is_banned(userid, username):
            return
        if self.manager_db.is_broker(userid, username):
            link = str(message.text).split(' ')
            if len(link) >= 2:
                link = link[1]
                if link.startswith("t.me") or link.startswith("https://t.me") or link.startswith("@"):
                    self.manager_db.set_link_broker(userid, username, link)
                    self.bot.send_message(
                        message.chat.id,
                        "Вы успешно установили свою ссылку на канал с отзывами!"
                    )
                else:
                    self.bot.send_message(
                        message.chat.id,
                        "Ссылка на канал с отзывами должна начинаться с t.me/, https://t.me или с @!",
                        disable_web_page_preview=True
                    )
            else:
                self.bot.send_message(
                    message.chat.id,
                    "Вы не ввели все параметры! Использование: `/линк [параметры]`",
                    parse_mode="Markdown",
                )
        else:
            self.send_no_access(
                message.chat.id,
                message.message_id,
                username,
                message.from_user.id,
                True,
            )

    def handle_text(self, message):
        userid = message.from_user.id
        username = message.from_user.username
        if self.manager_db.is_banned(userid, username):
            return
        self.manager_db.log_user(userid, username, message.chat.id)
        if self.manager_db.is_admin(userid, username):
            self.bot.send_message(
                message.chat.id,
                "Выберите действие:",
                reply_markup=self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
            )
        elif self.manager_db.is_broker(userid, username):
            self.bot.send_message(
                message.chat.id,
                "Выберите действие:",
                reply_markup=self.keyboards[1],
            )
        else:
            self.bot.send_message(
                message.chat.id,
                "Выберите действие:",
                reply_markup=self.keyboards[0],
            )

    def send_keyboard(self, keyboard, message_id, chat_id, text):
        try:
            self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=keyboard,
                disable_web_page_preview=True,
                parse_mode='HTML'
            )
        except ApiTelegramException as e:
            DatabaseManager.create_log(e)
            if e.error_code != 400:
                self.bot.send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)

    def chat_kick(self, message):
        if self.manager_db.is_admin(message.from_user.id, message.from_user.username):
            if message.reply_to_message is not None:
                if self.bot.bot_id != message.reply_to_message.from_user.id:
                    if self.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).is_member:
                        try:
                            self.bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                            self.bot.reply_to(message, "Пользователь был выгнан из группы!")
                        except ApiTelegramException:
                            self.bot.reply_to(message, "Я не назначен администратором, чтобы выполнить это действие!")
                    else:
                        self.bot.reply_to(message, "Пользователь не является участником группы!")

    def chat_ban(self, message):
        if self.manager_db.is_admin(message.from_user.id, message.from_user.username):
            if message.reply_to_message is not None:
                if self.bot.bot_id != message.reply_to_message.from_user.id:
                    if self.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).status != 'kicked':
                        try:
                            self.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                            self.bot.reply_to(message, "Пользователь успешно заблокирован в группе!")
                        except ApiTelegramException:
                            self.bot.reply_to(message, "Я не назначен администратором, чтобы выполнить это действие!")
                    else:
                        self.bot.reply_to(message, "Пользователь уже заблокирован в группе!")

    def chat_unban(self, message):
        if self.manager_db.is_admin(message.from_user.id, message.from_user.username):
            if message.reply_to_message is not None:
                if self.bot.bot_id != message.reply_to_message.from_user.id:
                    if self.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).status == 'kicked':
                        try:
                            self.bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                            self.bot.reply_to(message, "Пользователь был разблокирован в группе!")
                        except ApiTelegramException:
                            self.bot.reply_to(message, "Я не назначен администратором, чтобы выполнить это действие!")
                    else:
                        self.bot.reply_to(message, "Пользователь не заблокирован в группе!")

    def chat_mute(self, message):
        if self.manager_db.is_admin(message.from_user.id, message.from_user.username):
            if message.reply_to_message is not None:
                if self.bot.bot_id != message.reply_to_message.from_user.id:
                    if self.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).can_send_messages:
                        try:
                            self.bot.restrict_chat_member(
                                message.chat.id,
                                message.reply_to_message.from_user.id,
                                permissions=types.ChatPermissions(can_send_messages=False)
                            )
                            self.bot.delete_message(
                                message.chat.id,
                                message.reply_to_message.id,
                            )
                            self.bot.send_message(
                                message.chat.id,
                                f"Пользователь успешно замучен!"
                            )
                        except ApiTelegramException:
                            self.bot.send_message(
                                message.chat.id,
                                "Я не назначен администратором, чтобы выполнить это действие!"
                            )
                    else:
                        self.bot.send_message(
                            message.chat.id,
                            "Пользователь уже находится в муте!"
                        )

    def chat_unmute(self, message):
        if self.manager_db.is_admin(message.from_user.id, message.from_user.username):
            if message.reply_to_message is not None:
                if self.bot.bot_id != message.reply_to_message.from_user.id:
                    if not self.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).can_send_messages:
                        try:
                            self.bot.restrict_chat_member(
                                message.chat.id,
                                message.reply_to_message.from_user.id,
                                permissions=types.ChatPermissions(can_send_messages=True)
                            )
                            self.bot.send_message(
                                message.chat.id,
                                "Пользователь успешно размучен!"
                            )
                        except ApiTelegramException:
                            self.bot.send_message(
                                message.chat.id,
                                "Я не назначен администратором, чтобы выполнить это действие!"
                            )
                    else:
                        self.bot.send_message(
                            message.chat.id,
                            "Пользователь не находится в муте!"
                        )

    def send_log(self, text, username, userid):
        if username is None:
            link = f"tg://user?id={userid}"
        else:
            link = f"@{username}"
        try:
            self.bot.send_message(
                -1002447232743,
                f"Администратор ({link}) {text}",
                parse_mode="Markdown",
                disable_web_page_preview=True,
            )
        except ApiTelegramException as e:
            DatabaseManager.create_log(e)

    def send_no_access(self, chat_id, message_id, username, userid, keyboard=True):
        if keyboard:
            if self.manager_db.is_broker(userid, username):
                self.send_keyboard(
                    self.keyboards[1],
                    message_id,
                    chat_id,
                    "У вас нет доступа к этой команде!",
                )
            else:
                self.send_keyboard(
                    self.keyboards[0],
                    message_id,
                    chat_id,
                    "У вас нет доступа к этой команде!",
                )
        else:
            if self.manager_db.is_broker(userid, username):
                self.bot.send_message(
                    chat_id,
                    "У вас нет доступа к этой команде!",
                    reply_markup=self.keyboards[1],
                )
            else:
                self.bot.send_message(
                    chat_id,
                    "У вас нет доступа к этой команде!",
                    reply_markup=self.keyboards[0],
                )
