import os
import sqlite3
import sys
from sqlite3 import IntegrityError
from time import strftime, gmtime
from telebot.apihelper import ApiTelegramException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_normal_id(userid):
    if type(userid) != int:
        userid = 0
    return str(userid)


def get_normal_name(username):
    if type(username) is not str:
        username = ""
    else:
        if username.strip() == '':
            username = ""
        else:
            if not username.startswith("@"):
                username = f"@{username}"
    return username


def get_list(online_list, isset_text, empty_text):
    result = ""
    priority_result = ""
    for user in online_list:
        username = str(user[0])
        link = ""
        try:
            username = str(int(username))
            link = "tg://user?id="
        except ValueError:
            if not username.startswith("@"):
                link = "@"
        prefix = user[1]
        if type(prefix) is str and prefix.strip() != "":
            if prefix == "Владелец":
                if priority_result == "":
                    priority_result += link + username + " | " + prefix + "\n"
                else:
                    priority_result = link + username + " | " + prefix + "\n" + priority_result
                continue
            elif prefix == "Со-Владелец":
                priority_result += link + username + " | " + prefix + "\n"
                continue
            else:
                result += link + username + " | " + prefix + "\n"
        else:
            result += link + username + "\n"
    if result == "":
        return empty_text
    else:
        return isset_text + priority_result + result

def get_b_online(online_list, offset):
    if len(online_list) == 0:
        return None
    result = InlineKeyboardMarkup()
    for user in online_list:
        username = str(user[0])
        link = ""
        try:
            int(username)
        except ValueError:
            if not username.startswith("@"):
                link = "@"
        prefix = user[1]
        if type(prefix) is str and prefix.strip() != "":
            result.add(InlineKeyboardButton(
                link + username + " | " + prefix,
                callback_data="getbroker_"+username+f"_{offset}"
            ))
        else:
            result.add(InlineKeyboardButton(
                link + username,
                callback_data="getbroker_"+username+f"_{offset}"
            ))
    if (offset - len(online_list)) < 0:
        offsettt = 0
    else:
        if len(online_list) < 8:
            offsettt = offset - 8
        else:
            offsettt = offset - len(online_list)
    result.add(InlineKeyboardButton(
        "Назад",
        callback_data="cancelbrokers_"+str(offsettt),
    ),
    InlineKeyboardButton(
        "Далее",
        callback_data="nextbrokers_"+str((offset + len(online_list)))
    ))
    return result


def get_user(username):
    try:
        userid = int(username)
        return str(userid)
    except ValueError:
        return get_normal_name(username)


def create_log(error):
    if isinstance(error, ApiTelegramException):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log_text = (
            "["
            + strftime("%d.%m.%Y %H:%M:%S", gmtime())
            + f"] Произошла ошибка Telegram Bot API в файле '{os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]}' на строке {exc_tb.tb_lineno}! Функция: '{error.function_name}'. Код ошибки: '{error.error_code}'. Описание ошибки: '{error.description}'."
        )
        directory = os.path.dirname(__file__)
        with open(directory+"/../logs/Errors.log", "a") as myfile:
            myfile.write(log_text + "\n\n")
            myfile.close()


class DatabaseManager:
    def __init__(self):
        directory = os.path.dirname(__file__)
        self.db = sqlite3.connect(
            directory+"/../DataBase.sqlite3",
            check_same_thread=False,
        )
        self.cur = self.db.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS `admins` (`username` TEXT PRIMARY KEY, `is_online` BOOLEAN, `prefix` TEXT);"
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS `broker` (`username` TEXT PRIMARY KEY, `is_online` BOOLEAN, `prefix` TEXT, `link` TEXT, `deals_count` INT);"
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS `users` (`username` TEXT PRIMARY KEY, `chat_id` INTEGER);"
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS `bans` (`username` TEXT PRIMARY KEY, `reason` TEXT);"
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS `warns` (`username` TEXT PRIMARY KEY, `reason` TEXT, `count` INTEGER);"
        )
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS `deals` (`deal_id` INTEGER PRIMARY KEY);"
        )
        self.db.commit()
        self.owner_username = "sky4arg"

    def get_userid(self, username):
        username = self.get_normal_name(username)
        fetch_chat = self.cur.execute(
            "SELECT `chat_id` FROM `users` WHERE `username`=?", (username,)
        ).fetchone()
        if fetch_chat is not None:
            chat_id = fetch_chat[0]
        else:
            chat_id = 0
        return chat_id

    def log_user(self, userid, username, chat_id):
        username = get_normal_name(username)
        if username == "":
            username = get_normal_id(userid)
        if (
            self.cur.execute(
                "SELECT 1 FROM `users` WHERE `username` = ?", (username,)
            ).fetchone()
            is None
        ):
            self.cur.execute(
                "INSERT INTO `users` VALUES (?, ?)", (username, chat_id)
            )
            self.db.commit()
            return True
        else:
            return False

    def is_broker(self, userid, username=None):
        username = get_normal_name(username)
        if self.is_owner(username):
            return True
        userid = get_normal_id(userid)
        return (
            self.cur.execute(
                f"SELECT 1 FROM `broker` WHERE `username`=? OR `username`=?",
                (username, userid),
            ).fetchone()
            is not None
        )

    def get_online_brokers(self, start_num):
        online = self.cur.execute(
            "SELECT `username`,`prefix` FROM `broker` WHERE `is_online`=1 LIMIT 8 OFFSET ?", (start_num,)
        ).fetchall()
        return get_b_online(
            online,
            start_num,
        )

    def get_all_brokers(self):
        all_list = self.cur.execute(
            "SELECT `username`,`prefix` FROM `broker`;"
        ).fetchall()
        return get_list(
            all_list, "Список всех гарантов:\n\n", "Список гарантов пуст!"
        )

    def set_broker(self, username, broker):
        user = get_user(username)
        try:
            fetch_chat = self.cur.execute(
                "SELECT `chat_id` FROM `users` WHERE `username`=?", (user,)
            ).fetchone()
            if fetch_chat is not None:
                chat_id = fetch_chat[0]
            else:
                chat_id = 0
            if broker:
                self.cur.execute(
                    "INSERT INTO `broker` VALUES (?, FALSE, '', '', 0);", (user,)
                )
                self.db.commit()
                return ["yes", chat_id]
            else:
                if (
                    self.cur.execute(
                        "SELECT 1 FROM `broker` WHERE `username`=?", (user,)
                    ).fetchone()
                    is not None
                ):
                    self.cur.execute(
                        "DELETE FROM `broker` WHERE `username`=?;", (user,)
                    )
                    self.db.commit()
                    return ["yes", chat_id]
                else:
                    return ["no"]
        except IntegrityError:
            return ["no"]

    def set_online_broker(self, userid, username, online):
        username = get_normal_name(username)
        if username == "":
            username = get_normal_id(userid)
        fetch = self.cur.execute(
            "SELECT `is_online` FROM `broker` WHERE `username`=?", (username,)
        ).fetchone()
        if fetch is not None:
            if fetch[0] != online:
                self.cur.execute(
                    "UPDATE `broker` SET `is_online`=? WHERE `username`=?",
                    (online, username),
                )
                self.db.commit()
                return 0
            else:
                return -1
        else:
            return -2

    def set_prefix_broker(self, username, prefix):
        user = get_user(username)
        if (
            self.cur.execute(
                "SELECT 1 FROM `broker` WHERE `username`=?", (user,)
            ).fetchone()
            is not None
        ):
            self.cur.execute(
                f"UPDATE `broker` SET `prefix`=? WHERE `username`=?;",
                (prefix, user),
            )
            self.db.commit()
            return True
        else:
            return False

    def set_link_broker(self, userid, username, link):
        user = get_normal_name(username)
        if username == "":
            user = get_normal_id(userid)
        if (
            self.cur.execute(
                "SELECT 1 FROM `broker` WHERE `username`=?", (user,)
            ).fetchone()
            is not None
        ):
            self.cur.execute(
                f"UPDATE `broker` SET `link`=? WHERE `username`=?;",
                (link, user),
            )
            self.db.commit()
            return True
        else:
            return False

    def get_link_broker(self, userid, username):
        user = get_normal_name(username)
        if username == "":
            user = get_normal_id(userid)
        link = self.cur.execute(
            "SELECT `link` FROM `broker` WHERE `username`=?", (user,)
        ).fetchone()
        if link is not None:
            link = str(link[0])
            if link.strip() != '':
                if link.startswith('t.me') or link.startswith('https://t.me') or link.startswith('@'):
                    return link
        return "Отсутствует"

    def get_deal_broker(self, userid, username):
        user = get_normal_name(username)
        if username == "":
            user = get_normal_id(userid)
        count_deal = self.cur.execute("SELECT `deals_count` FROM `broker` WHERE `username`=?", (user,)).fetchone()
        if count_deal is not None:
            return count_deal[0]
        else:
            return 0

    def add_deal_broker(self, userid, username):
        user = get_normal_name(username)
        if username == "":
            user = get_normal_id(userid)
        count_deals = self.cur.execute("SELECT `deals_count` FROM `broker` WHERE `username`=?", (user, )).fetchone()
        if count_deals is not None:
            count_deals = count_deals[0]
            count_deals += 1
            self.cur.execute(
                "UPDATE `broker` SET `deals_count`=? WHERE `username`=?",
                (count_deals, user),
            )
            self.db.commit()
            return True
        else:
            return False

    def get_all_chat_id_brokers(self):
        result = []
        all_brokers = self.cur.execute(
            "SELECT `username` FROM `broker`;"
        ).fetchall()
        for user in all_brokers:
            chat_id = self.cur.execute(
                "SELECT `chat_id` FROM `users` WHERE `username`=?;", (user[0],)
            ).fetchone()
            if (
                chat_id is not None
                and type(chat_id) == tuple
                and type(chat_id[0]) == int
            ):
                result.append(chat_id[0])
        return result

    def get_all_chat_id_users(self):
        result = []
        chat_ids = self.cur.execute(
            "SELECT `chat_id` FROM `users`"
        ).fetchall()
        for chat_id in chat_ids:
            if chat_id is not None:
                if type(chat_id) == tuple or type(chat_id) is dict:
                    result.append(chat_id[0])
                else:
                    result.append(chat_id[0])
        return result

    def is_admin(self, userid, username=None):
        username = get_normal_name(username)
        if self.is_owner(username.lstrip('@')):
            return True
        userid = get_normal_id(userid)
        return (
            self.cur.execute(
                f"SELECT 1 FROM `admins` WHERE `username`=? OR `username`=?",
                (username, userid),
            ).fetchone()
            is not None
        )

    def get_all_admins(self):
        all_list = self.cur.execute(
            "SELECT `username`,`prefix` FROM `admins`;"
        ).fetchall()
        return get_list(
            all_list, "Список всех админов:\n\n", "Список админов пуст!"
        )

    def set_admin(self, username, admin):
        user = get_user(username)
        try:
            fetch_chat = self.cur.execute(
                "SELECT `chat_id` FROM `users` WHERE `username`=?", (user,)
            ).fetchone()
            if fetch_chat is not None:
                chat_id = fetch_chat[0]
            else:
                chat_id = 0
            if admin:
                self.cur.execute(
                    f"INSERT INTO `admins` VALUES (?, FALSE, '');", (user,)
                )
                self.db.commit()
                return ["yes", chat_id]
            else:
                if (
                    self.cur.execute(
                        f"SELECT 1 FROM `admins` WHERE `username`=?", (user,)
                    ).fetchone()
                    is not None
                ):
                    self.cur.execute(
                        f"DELETE FROM `admins` WHERE `username`=?;", (user,)
                    )
                    self.db.commit()
                    return ["yes", chat_id]
                else:
                    return ["no"]
        except IntegrityError:
            return ["no"]

    def set_prefix_admin(self, username, prefix):
        user = get_user(username)
        if (
            self.cur.execute(
                "SELECT 1 FROM `admins` WHERE `username`=?", (user,)
            ).fetchone()
            is not None
        ):
            self.cur.execute(
                f"UPDATE `admins` SET `prefix`=? WHERE `username`=?;",
                (prefix, user),
            )
            self.db.commit()
            return True
        else:
            return False

    def ban_user(self, username, reason):
        user = get_user(username)
        try:
            self.cur.execute("INSERT INTO `bans` VALUES (?,?);", (user, reason))
            self.db.commit()
            fetch_chat = self.cur.execute(
                "SELECT `chat_id` FROM `users` WHERE `username`=?", (user,)
            ).fetchone()
            if fetch_chat is not None:
                chat_id = fetch_chat[0]
            else:
                chat_id = 0
            return ["yes", chat_id]
        except IntegrityError:
            return ["no"]

    def unban_user(self, username):
        user = get_user(username)
        if (
            self.cur.execute(
                "SELECT 1 FROM `bans` WHERE `username`=?", (user,)
            ).fetchone()
            is not None
        ):
            self.cur.execute("DELETE FROM `bans` WHERE `username`=?;", (user,))
            self.cur.execute(
                "DELETE FROM `warns` WHERE `username`=? AND `count`=3;", (user,)
            )
            self.db.commit()
            fetch_chat = self.cur.execute(
                "SELECT `chat_id` FROM `users` WHERE `username`=?", (user,)
            ).fetchone()
            if fetch_chat is not None:
                chat_id = fetch_chat[0]
            else:
                chat_id = 0
            return ["yes", chat_id]
        else:
            return ["no"]

    def is_banned(self, userid, username):
        username = get_normal_name(username)
        if self.is_owner(username):
            return False
        userid = get_normal_id(userid)
        return (
            self.cur.execute(
                f"SELECT 1 FROM `bans` WHERE `username`=? OR `username`=?",
                (username, userid),
            ).fetchone()
            is not None
        )

    def warn_user(self, username, reason):
        user = get_user(username)
        fetch = self.cur.execute(
            "SELECT `count`,`reason` FROM `warns` WHERE `username`=?", (user,)
        ).fetchone()
        fetch_chat = self.cur.execute(
            "SELECT `chat_id` FROM `users` WHERE `username`=?", (user,)
        ).fetchone()
        if fetch_chat is not None:
            chat_id = fetch_chat[0]
        else:
            chat_id = 0
        if fetch is not None:
            if fetch[0] == 3:
                return ["banned"]
            count = fetch[0] + 1
            self.cur.execute(
                "UPDATE `warns` SET `count`=?, `reason`=? WHERE `username`=?;",
                (count, reason, user),
            )
            self.db.commit()
            if fetch[0] == 2:
                try:
                    self.cur.execute(
                        "INSERT INTO `bans` VALUES (?,?);", (user, reason)
                    )
                    self.db.commit()
                except IntegrityError:
                    pass
                return ["ban", 3, chat_id]
            else:
                return ["warn", count, chat_id]
        else:
            self.cur.execute(
                "INSERT INTO `warns` VALUES (?,?,?);", (user, reason, 1)
            )
            self.db.commit()
            return ["warn", 1, chat_id]

    def unwarn_user(self, username):
        user = get_user(username)
        result = self.cur.execute(
            "SELECT `count` FROM `warns` WHERE `username`=?", (user,)
        ).fetchone()
        if result is not None:
            fetch_chat = self.cur.execute(
                "SELECT `chat_id` FROM `users` WHERE `username`=?", (user,)
            ).fetchone()
            if fetch_chat is not None:
                chat_id = fetch_chat[0]
            else:
                chat_id = 0
            if result[0] == 1:
                self.cur.execute(
                    "DELETE FROM `warns` WHERE `username`=?;", (user,)
                )
                self.db.commit()
                return ["yes", chat_id, 0]
            elif result[0] == 3:
                return ["banned"]
            elif result[0] == 2:
                self.cur.execute(
                    "UPDATE `warns` SET `count`=1 WHERE `username`=?;", (user,)
                )
                self.db.commit()
                return ["yes", chat_id, 1]
            else:
                return ["no"]
        else:
            return ["no"]

    def is_owner(self, username):
        return username == self.owner_username or username == 'luckydevv' or username == '@luckydevv'

    def get_user_tgname(self, username):
        try:
            userid = int(username)
            return "tg://user?id={}".format(userid)
        except ValueError:
            return get_normal_name(username)

    def get_normal_id(self, userid):
        if type(userid) != int:
            userid = 0
        return str(userid)

    def get_normal_name(self, username):
        if type(username) is not str:
            username = ""
        else:
            if not username.startswith("@"):
                username = f"@{username}"
        return username
