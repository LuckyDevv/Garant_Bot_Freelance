from telebot.apihelper import ApiTelegramException

from Utils import DatabaseManager


class QueryHandler:
    def __init__(self, bot, manager_db, user_kb, grant_kb, admin_kb, ab_kb):
        self.bot = bot
        self.manager_db = manager_db
        self.keyboards = [user_kb, grant_kb, admin_kb, ab_kb]

    def cancel_online_brokers(self, call, userid, username):
        self.bot.answer_callback_query(call.id)
        if self.manager_db.is_admin(userid, username):
            self.send_keyboard(
                self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                call.message.message_id,
                call.message.chat.id,
                "Выберите действие",
            )
        elif self.manager_db.is_broker(userid, username):
            self.send_keyboard(
                self.keyboards[1],
                call.message.message_id,
                call.message.chat.id,
                "Выберите действие",
            )
        else:
            self.send_keyboard(
                self.keyboards[0],
                call.message.message_id,
                call.message.chat.id,
                "Выберите действие",
            )

    def broker_online_list_next(self, call, userid, username, offset):
        self.bot.answer_callback_query(call.id)
        result = self.manager_db.get_online_brokers(offset)
        if result is not None:
            kb = result
            messag = "Список гарантов онлайн:"
            if (self.send_keyboard(
                kb,
                call.message.message_id,
                call.message.chat.id,
                messag,
                True
            )):
                self.cancel_online_brokers(call, userid, username)

    def broker_online_list(self, call, userid, username):
        result = self.manager_db.get_online_brokers(0)
        self.bot.answer_callback_query(call.id)
        if result is None:
            messag = "Сейчас нет гарантов онлайн."
            kb = None
        else:
            kb = result
            messag = "Список гарантов онлайн:"
        if self.manager_db.is_admin(userid, username):
            self.send_keyboard(
                (self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2]) if kb is None else kb,
                call.message.message_id,
                call.message.chat.id,
                messag,
            )
        elif self.manager_db.is_broker(userid, username):
            self.send_keyboard(
                self.keyboards[1] if kb is None else kb,
                call.message.message_id,
                call.message.chat.id,
                messag,
            )
        else:
            self.send_keyboard(
                self.keyboards[0] if kb is None else kb,
                call.message.message_id,
                call.message.chat.id,
                messag,
            )

    def broker_all_list(self, call, userid, username):
        self.bot.answer_callback_query(call.id)
        if self.manager_db.is_admin(userid, username):
            self.send_keyboard(
                self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                call.message.message_id,
                call.message.chat.id,
                self.manager_db.get_all_brokers(),
            )
        else:
            self.send_no_access(
                call.message.chat.id, call.message.message_id, username, userid
            )

    def broker_online(self, call, userid, username):
        result = self.manager_db.set_online_broker(userid, username, True)
        self.bot.answer_callback_query(call.id)
        if result == 0:
            self.send_keyboard(
                self.keyboards[3] if self.manager_db.is_admin(userid, username) else self.keyboards[1],
                call.message.message_id,
                call.message.chat.id,
                "Вы успешно вошли в онлайн!",
            )
        elif result == -1:
            self.send_keyboard(
                self.keyboards[3] if self.manager_db.is_admin(userid, username) else self.keyboards[1],
                call.message.message_id,
                call.message.chat.id,
                "Вы уже находитесь в онлайне!",
            )
        else:
            if self.manager_db.is_admin(userid, username):
                self.send_keyboard(
                    self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    call.message.message_id,
                    call.message.chat.id,
                    "У вас нет доступа к этой команде!",
                )
            else:
                self.send_keyboard(
                    self.keyboards[0],
                    call.message.message_id,
                    call.message.chat.id,
                    "У вас нет доступа к этой команде!",
                )

    def broker_offline(self, call, userid, username):
        result = self.manager_db.set_online_broker(userid, username, False)
        self.bot.answer_callback_query(call.id)
        if result == 0:
            self.send_keyboard(
                self.keyboards[3] if self.manager_db.is_admin(userid, username) else self.keyboards[1],
                call.message.message_id,
                call.message.chat.id,
                "Вы успешно вышли в оффлайн!",
            )
        elif result == -1:
            self.send_keyboard(
                self.keyboards[3] if self.manager_db.is_admin(userid, username) else self.keyboards[1],
                call.message.message_id,
                call.message.chat.id,
                "Вы уже находитесь в оффлайне!",
            )
        else:
            if self.manager_db.is_admin(userid, username):
                self.send_keyboard(
                    self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                    call.message.message_id,
                    call.message.chat.id,
                    "У вас нет доступа к этой команде!",
                )
            else:
                self.send_keyboard(
                    self.keyboards[0],
                    call.message.message_id,
                    call.message.chat.id,
                    "У вас нет доступа к этой команде!",
                )

    def admin_all_list(self, call, userid, username):
        self.bot.answer_callback_query(call.id)
        if self.manager_db.is_admin(userid, username):
            self.send_keyboard(
                self.keyboards[3] if self.manager_db.is_broker(userid, username) else self.keyboards[2],
                call.message.message_id,
                call.message.chat.id,
                self.manager_db.get_all_admins(),
            )
        else:
            self.send_no_access(
                call.message.chat.id, call.message.message_id, username, userid
            )

    def send_keyboard(self, keyboard, message_id, chat_id, text, iscancel=False):
        try:
            self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=keyboard,
            )
        except ApiTelegramException as e:
            if iscancel:
                return True
            else:
                DatabaseManager.create_log(e)
                if e.error_code != 400:
                    self.bot.send_message(chat_id, text, reply_markup=keyboard)

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
