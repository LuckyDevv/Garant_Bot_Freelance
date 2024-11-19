from telebot.apihelper import ApiTelegramException

import DatabaseManager


class QueryHandler:
    def __init__(self, bot, manager_db, user_kb, grant_kb, admin_kb):
        self.bot = bot
        self.manager_db = manager_db
        self.keyboards = [user_kb, grant_kb, admin_kb]

    def broker_online_list(self, call, userid, username):
        result = self.manager_db.get_online_brokers()
        self.bot.answer_callback_query(call.id)
        if self.manager_db.is_admin(userid, username):
            self.send_keyboard(
                self.keyboards[2],
                call.message.message_id,
                call.message.chat.id,
                result,
            )
        elif self.manager_db.is_broker(userid, username):
            self.send_keyboard(
                self.keyboards[1],
                call.message.message_id,
                call.message.chat.id,
                result,
            )
        else:
            self.send_keyboard(
                self.keyboards[0],
                call.message.message_id,
                call.message.chat.id,
                result,
            )

    def broker_all_list(self, call, userid, username):
        self.bot.answer_callback_query(call.id)
        if self.manager_db.is_admin(userid, username):
            self.send_keyboard(
                self.keyboards[2],
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
                self.keyboards[1],
                call.message.message_id,
                call.message.chat.id,
                "Вы успешно вошли в онлайн!",
            )
        elif result == -1:
            self.send_keyboard(
                self.keyboards[1],
                call.message.message_id,
                call.message.chat.id,
                "Вы уже онлайн!",
            )
        else:
            if self.manager_db.is_admin(userid, username):
                self.send_keyboard(
                    self.keyboards[2],
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
                self.keyboards[1],
                call.message.message_id,
                call.message.chat.id,
                "Вы успешно ушли в оффлайн!",
            )
        elif result == -1:
            self.send_keyboard(
                self.keyboards[1],
                call.message.message_id,
                call.message.chat.id,
                "Вы уже оффлайн!",
            )
        else:
            if self.manager_db.is_admin(userid, username):
                self.send_keyboard(
                    self.keyboards[2],
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

    def admin_online_list(self, call, userid, username):
        result = self.manager_db.get_online_admins()
        self.bot.answer_callback_query(call.id)
        if self.manager_db.is_admin(userid, username):
            self.send_keyboard(
                self.keyboards[2],
                call.message.message_id,
                call.message.chat.id,
                result,
            )
        elif self.manager_db.is_broker(userid, username):
            self.send_keyboard(
                self.keyboards[1],
                call.message.message_id,
                call.message.chat.id,
                result,
            )
        else:
            self.send_keyboard(
                self.keyboards[0],
                call.message.message_id,
                call.message.chat.id,
                result,
            )

    def admin_all_list(self, call, userid, username):
        self.bot.answer_callback_query(call.id)
        if self.manager_db.is_admin(userid, username):
            self.send_keyboard(
                self.keyboards[2],
                call.message.message_id,
                call.message.chat.id,
                self.manager_db.get_all_admins(),
            )
        else:
            self.send_no_access(
                call.message.chat.id, call.message.message_id, username, userid
            )

    def admin_online(self, call, userid, username):
        result = self.manager_db.set_online_admin(userid, username, True)
        self.bot.answer_callback_query(call.id)
        if result == 0:
            self.send_keyboard(
                self.keyboards[2],
                call.message.message_id,
                call.message.chat.id,
                "Вы успешно вошли в онлайн!",
            )
        elif result == -1:
            self.send_keyboard(
                self.keyboards[2],
                call.message.message_id,
                call.message.chat.id,
                "Вы уже онлайн!",
            )
        else:
            if self.manager_db.is_broker(userid, username):
                self.send_keyboard(
                    self.keyboards[1],
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

    def admin_offline(self, call, userid, username):
        result = self.manager_db.set_online_admin(userid, username, False)
        self.bot.answer_callback_query(call.id)
        if result == 0:
            self.send_keyboard(
                self.keyboards[2],
                call.message.message_id,
                call.message.chat.id,
                "Вы успешно ушли в оффлайн!",
            )
        elif result == -1:
            self.send_keyboard(
                self.keyboards[2],
                call.message.message_id,
                call.message.chat.id,
                "Вы уже оффлайн!",
            )
        else:
            if self.manager_db.is_broker(userid, username):
                self.send_keyboard(
                    self.keyboards[1],
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

    def send_keyboard(self, keyboard, message_id, chat_id, text):
        try:
            self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=keyboard,
            )
        except ApiTelegramException as e:
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
