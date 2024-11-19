from os import mkdir
from os.path import exists

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard(kb_type):
    if kb_type == "user":
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                "Список онлайн гарантов", callback_data="broker_online_list"
            ),
            InlineKeyboardButton(
                "Список онлайн админов", callback_data="admin_online_list"
            ),
        )
    elif kb_type == "broker":
        return (
            InlineKeyboardMarkup()
            .add(
                InlineKeyboardButton(
                    "Список онлайн гарантов", callback_data="broker_online_list"
                ),
                InlineKeyboardButton(
                    "Список онлайн админов", callback_data="admin_online_list"
                ),
            )
            .add(
                InlineKeyboardButton(
                    "Я онлайн (Гарант)", callback_data="broker_online"
                ),
                InlineKeyboardButton(
                    "Я оффлайн (Гарант)", callback_data="broker_offline"
                ),
            )
        )
    elif kb_type == "admin":
        return (
            InlineKeyboardMarkup()
            .add(
                InlineKeyboardButton(
                    "Список онлайн гарантов", callback_data="broker_online_list"
                ),
                InlineKeyboardButton(
                    "Список всех гарантов", callback_data="broker_all_list"
                ),
            )
            .add(
                InlineKeyboardButton(
                    "Список онлайн админов", callback_data="admin_online_list"
                ),
                InlineKeyboardButton(
                    "Список всех админов", callback_data="admin_all_list"
                ),
            )
            .add(
                InlineKeyboardButton(
                    "Я онлайн (Админ)", callback_data="admin_online"
                ),
                InlineKeyboardButton(
                    "Я оффлайн (Админ)", callback_data="admin_offline"
                ),
            )
        )
    elif kb_type == "admin_broker":
        return (
            InlineKeyboardMarkup()
            .add(
                InlineKeyboardButton(
                    "Список онлайн гарантов", callback_data="broker_online_list"
                ),
                InlineKeyboardButton(
                    "Список всех гарантов", callback_data="broker_all_list"
                ),
            )
            .add(
                InlineKeyboardButton(
                    "Список онлайн админов", callback_data="admin_online_list"
                ),
                InlineKeyboardButton(
                    "Список всех админов", callback_data="admin_all_list"
                ),
            )
            .add(
                InlineKeyboardButton(
                    "Я онлайн (Админ)", callback_data="admin_online"
                ),
                InlineKeyboardButton(
                    "Я оффлайн (Админ)", callback_data="admin_offline"
                ),
            )
            .add(
                InlineKeyboardButton(
                    "Я онлайн (Гарант)", callback_data="broker_online"
                ),
                InlineKeyboardButton(
                    "Я оффлайн (Гарант)", callback_data="broker_offline"
                ),
            )
        )


def create_dirs():
    if not exists("/home/luckydevv"):
        mkdir("/home/luckydevv")
    if not exists("/home/luckydevv/broker_bot"):
        mkdir("/home/luckydevv/broker_bot")
