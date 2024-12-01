import os

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_broker_keyboard(user_id):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            "Принять",
            callback_data=f"brokeraccept_{user_id}",
        ),
        InlineKeyboardButton(
            "Отклонить",
            callback_data=f"brokerreject_{user_id}",
        )
    )

def get_user_keyboard(broker_id):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            "Отменить сделку",
            callback_data=f"canceldeal_{broker_id}",
        )
    )

def get_deal_keyboard(chat_id, user_id):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            "Завершить сделку",
            callback_data=f"enddeal_{chat_id}_{user_id}",
        )
    )

def get_broker_deal_keyboard(broker_id, offset):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            "Назад",
            callback_data=f"nextbrokers_{offset}",
        ),
        InlineKeyboardButton(
            "Запросить сделку",
            callback_data=f"requestdeal_{broker_id}",
        )
    )

def get_keyboard(kb_type):
    if kb_type == "user":
        return InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                "Список онлайн гарантов", callback_data="broker_online_list"
            ),
            InlineKeyboardButton(
                "Список администраторов", callback_data="admin_all_list"
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
                    "Список администраторов", callback_data="admin_all_list"
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
                    "Список администраторов", callback_data="admin_all_list"
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
                    "Список администраторов", callback_data="admin_all_list"
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


def create_dirs(directory):
    if not os.path.exists(directory+"/configs"):
        os.makedirs(directory+"/configs")
    if not os.path.exists(directory+"/logs"):
        os.makedirs(directory+"/logs")

