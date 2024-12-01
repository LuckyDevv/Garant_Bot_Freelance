import os
import threading
from time import strftime, gmtime
import telebot
from telebot.apihelper import ApiTelegramException

from Utils.ConfigController import ConfigController, ConfigType
from Utils.CommandHandler import CommandHandler
from Utils.DatabaseManager import DatabaseManager
from Utils import Initializer
from Utils.QueryHandler import QueryHandler
import atexit


TOKEN = "7579498106:AAGbTmMeeP9JrbWTMUFIr8a6kDl9xmprQDo"  # Введите сюда токен своего Telegram-бота
bot = telebot.TeleBot(TOKEN)
bot.set_webhook()
directory = os.path.dirname(__file__)
Initializer.create_dirs(directory)
users_ttd = ConfigController(directory+"/configs/users_to_do_deal.json", ConfigType.JSON)
users_deal = ConfigController(directory+"/configs/users_deal.json", ConfigType.JSON)
users_groups = ConfigController(directory+"/configs/users_groups.json", ConfigType.JSON)


def msg_log(message):
    message = message+strftime("%d.%m.%Y %H:%M:%S", gmtime())
    with open(directory+"/logs/Work.log", "a") as myfile:
        myfile.write(message+"\n\n")
        myfile.close()
        try:
            bot.send_message(1199296238, message)
        except:
            pass


atexit.register(
    msg_log,
    "Скрипт завершил свою работу в "
)
msg_log("Скрипт запущен в ")

user_keyboard = Initializer.get_keyboard("user")
broker_keyboard = Initializer.get_keyboard("broker")
admin_keyboard = Initializer.get_keyboard("admin")
ab_keyboard = Initializer.get_keyboard("admin_broker")

database_manager = DatabaseManager()
command_handler = CommandHandler(
    bot,
    database_manager,
    user_keyboard,
    broker_keyboard,
    admin_keyboard,
    ab_keyboard,
)
query_handler = QueryHandler(
    bot,
    database_manager,
    user_keyboard,
    broker_keyboard,
    admin_keyboard,
    ab_keyboard,
)

commands = {
    "/add_broker": command_handler.add_broker,
    "/remove_broker": command_handler.remove_broker,
    "/add_admin": command_handler.add_admin,
    "/remove_admin": command_handler.remove_admin,
    "/set_prefix": command_handler.set_prefix,
    "/ban": command_handler.ban_user,
    "/warn": command_handler.warn_user,
    "/unban": command_handler.unban_user,
    "/unwarn": command_handler.unwarn_user,
    "/mail": command_handler.mail_send,
    "/set_link": command_handler.set_link,
}

chat_commands = {
    "/ckick": command_handler.chat_kick,
    "/cban": command_handler.chat_ban,
    "/cunban": command_handler.chat_unban,
}

queries = {
    "broker_online_list": query_handler.broker_online_list,
    "broker_all_list": query_handler.broker_all_list,
    "broker_online": query_handler.broker_online,
    "broker_offline": query_handler.broker_offline,
    "admin_all_list": query_handler.admin_all_list,
}


@bot.message_handler(content_types=["text"])
def t1(message):
    command = message.text.split()[0]
    if message.chat.type == "private":
        if command in commands:
            commands[command](message)
        else:
            command_handler.handle_text(message)
    elif message.chat.type == "group" or message.chat.type == "supergroup":
        if command == '/check_group':
            if users_groups.exists(message.from_user.id):
                try:
                    link = bot.export_chat_invite_link(message.chat.id)
                    bot.send_message(
                        users_groups.get(message.from_user.id),
                        f"Пользователь успешно создал группу. Пригласительная ссылка для присоединения к группе: {link}"
                            f"\n\nПосле завершения сделки нажмите кнопку «Завершить сделку»."
                            f"\nПри нажатии на кнопку бот автоматически удалит вас из группы для вашего удобства.",
                            reply_markup=Initializer.get_deal_keyboard(message.chat.id, message.from_user.id))
                    bot.send_message(
                        message.chat.id,
                        "Пригласительная ссылка успешно отправлена гаранту."
                        "Пожалуйста, ожидайте, пока гарант вступит в группу. Сделка начнётся автоматически.",
                        disable_web_page_preview=True
                    )
                    users_groups.remove(message.from_user.id)
                    users_groups.save()
                    users_deal.set(message.from_user.id)
                    users_deal.save()
                except ApiTelegramException:
                    bot.send_message(message.chat.id, "Вы должны назначить меня администратором!")
        else:
            if command in chat_commands:
                chat_commands[command](message)



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
    else:
        datal = str(call.data).split("_")
        if datal[0] == "getbroker":
            bot.answer_callback_query(call.id)
            if len(datal) == 3:
                brokerid = datal[1]
                command_handler.send_keyboard(
                    Initializer.get_broker_deal_keyboard(brokerid, int(datal[2])),
                    call.message.id,
                    call.message.chat.id,
                    f"Информация о гаранте {brokerid}:"
                    f"\n\nКол-во сделок: {database_manager.get_deal_broker(brokerid, brokerid)}"
                    f"\nГруппа с отзывами: {database_manager.get_link_broker(brokerid, brokerid)}"
                    f"\n\nЕсли вы хотите, чтобы этот гарант провел с вами сделку, нажмите кнопку «Запросить сделку»."
                )
        elif datal[0] == "requestdeal":
            bot.answer_callback_query(call.id)
            brokerid = datal[1]
            if brokerid == username or brokerid == userid or brokerid == '@'+username:
                bot.send_message(
                    call.message.chat.id,
                    "Нельзя запрашивать сделку у самого себя!"
                )
                return
            if not users_ttd.exists(userid):
                command_handler.send_keyboard(
                    None,
                    call.message.id,
                    call.message.chat.id,
                    f"Вы выбрали гаранта {brokerid}."
                    f"\n\nНапишите здесь суть сделки одним сообщением; оно будет передано гаранту."
                )
                bot.register_next_step_handler_by_chat_id(
                    call.message.chat.id, send_broker_msg, brokerid)
            else:
                command_handler.send_keyboard(
                    None,
                    call.message.id,
                    call.message.chat.id,
                    "Вы уже недавно отправляли запрос гаранту. "
                    "Перед следующим запросом необходимо подождать 5 минут с момента отправления предыдущего запроса!",
                )
        elif datal[0] == "nextbrokers":
            bot.answer_callback_query(call.id)
            try:
                query_handler.broker_online_list_next(
                    call, userid, username, int(datal[1])
                )
            except ValueError:
                return
        elif datal[0] == "cancelbrokers":
            if len(datal) == 2:
                query_handler.broker_online_list_next(
                    call, userid, username, int(datal[1])
                )
            else:
                query_handler.cancel_online_brokers(call, userid, username)
        elif datal[0] == "brokeraccept":
            bot.answer_callback_query(call.id)
            if len(datal) == 2:
                if database_manager.is_broker(userid, username):
                    user_id = int(datal[1])
                    command_handler.send_keyboard(
                        None,
                        call.message.id,
                        call.message.chat.id,
                        "Вы успешно приняли обращение от пользователя. "
                        "Ожидайте, пока пользователь самостоятельно создаст группу и добавит туда бота. "
                        "После этого вам будет отправлена пригласительная ссылка в эту группу."
                    )
                    bot.send_message(
                        user_id,
                        "Гарант принял ваш запрос."
                        "\n\nТеперь самостоятельно создайте группу для проведения сделки."
                        "В названии группы не должно быть нецензурной лексики и оскорбительных фраз."
                        "\n\nПосле создания группы добавьте в неё второго участника и этого бота."
                        "\n\nПосле добавления назначьте бота администратором и введите команду `/check_group` в этой группе."
                        "\n\nБот автоматически проверит группу и отправит гаранту пригласительную ссылку."
                        "\n\n\nЕсли вы передумали проводить сделку, нажмите кнопку «Отменить сделку».",
                        reply_markup=Initializer.get_user_keyboard(
                            call.message.chat.id
                        ),
                        parse_mode="Markdown",
                    )
                    users_groups.set(user_id, call.message.chat.id)
                    users_groups.save()
        elif datal[0] == "brokerreject":
            bot.answer_callback_query(call.id)
            if len(datal) == 2:
                user_id = int(datal[1])
                if users_deal.exists(userid):
                    if database_manager.is_broker(userid, username):
                        bot.send_message(
                            user_id,
                            "Гарант отклонил ваш запрос. Вы можете выбрать другого гаранта для проведения сделки.",
                        )
                        command_handler.send_keyboard(
                            None,
                            call.message.id,
                            call.message.chat.id,
                            "Вы успешно отклонили обращение от пользователя."
                        )
        elif datal[0] == "canceldeal":
            bot.answer_callback_query(call.id)
            if users_groups.exists(call.message.chat.id):
                if len(datal) == 2:
                    broker_id = int(datal[1])
                    bot.send_message(
                        call.message.chat.id, "Вы успешно отменили сделку."
                    )
                    bot.send_message(broker_id, "Пользователь отменил сделку.")
                    users_groups.remove(call.message.chat.id)
                    users_groups.save()
        elif datal[0] == "enddeal":
            bot.answer_callback_query(call.id)
            if len(datal) == 3:
                userid = int(datal[2])
                if users_deal.exists(userid):
                    database_manager.add_deal_broker(call.from_user.id, call.from_user.username)
                    try:
                        bot.send_message(call.message.chat.id,
                                         "Вы успешно завершили сделку. Спасибо за использование нашей платформы!\n\nЕсли вы считаете, что пользователь нарушил правила платформы, обратитесь к нашим администраторам!")
                        bot.send_message(int(datal[2]),
                                         "Гарант завершил сделку. Спасибо за использование нашей платформы!\n\nЕсли вы считаете, что гарант нарушил правила платформы и/или преждевременно закрыл сделку, обратитесь к нашим администраторам!")
                        bot.send_message(int(datal[1]),
                                         "Гарант завершил сделку. Теперь вы можете удалить группу. Спасибо за использование нашей платформы!")
                        bot.unban_chat_member(int(datal[1]), call.message.chat.id)
                        bot.leave_chat(int(datal[1]))
                    except ApiTelegramException:
                        pass
                    users_deal.remove(userid)
                    users_deal.save()
                    users_ttd.remove(userid)
                    users_ttd.save()


def send_broker_msg(message, broker_id):
    broker_id = database_manager.get_userid(broker_id)
    try:
        bot.send_message(
            broker_id,
            f"Поступило новое обращение от потенциального клиента:\n\n«{message.text}»\n\nЧтобы принять обращение, нажмите «Принять», чтобы отклонить — «Отклонить».",
            reply_markup=Initializer.get_broker_keyboard(message.chat.id),
        )
        bot.send_message(
            message.chat.id,
            "Сообщение успешно доставлено гаранту! Ожидайте ответа...",
        )
        users_ttd.set(message.chat.id)
        threading.Timer(300, flush_userid, (message.chat.id,)).start()
    except ApiTelegramException:
        bot.send_message(
            message.chat.id,
            "Не удалось отправить сообщение гаранту. Вы можете выбрать другого гаранта для проведения сделки.",
        )


def create_deal_group(message, broker_name):
    if users_deal.exists(message.chat.id):
        broker_name = broker_name[0]
        broker_id = database_manager.get_userid(broker_name)
        if str(message.text).startswith('@'):
            pass
        else:
            bot.send_message(message.chat.id, "Юзернейм должен начинаться с @! Попробуйте ещё раз...")
            bot.register_next_step_handler_by_chat_id(message.chat.id, create_deal_group, (broker_id, ))


def flush_userid(user_id):
    users_ttd.remove(user_id)
    users_ttd.save()


bot.infinity_polling(timeout=10, long_polling_timeout=5)
