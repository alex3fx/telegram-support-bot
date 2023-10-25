import os
from telegram.ext import CommandHandler, MessageHandler, Filters

from settings import WELCOME_MESSAGE, TELEGRAM_SUPPORT_CHAT_ID, REPLY_TO_THIS_MESSAGE, WRONG_REPLY

users = set() # Простое хранилище chat_id пользователей. В реальном приложении лучше использовать БД.

def save_chat_id_to_file(chat_id, filename='chat_ids.txt'):
    """Сохраняет chat_id в файл."""
    with open(filename, 'a') as file:
        file.write(str(chat_id) + '\n')

def load_chat_ids_from_file(filename='chat_ids.txt'):
    """Загружает все chat_ids из файла."""
    chat_ids = set()
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                chat_ids.add(int(line.strip()))
    except FileNotFoundError:
        pass
    return chat_ids

def users_init():
    """Загружает chat_ids из файла."""
    global users
    users = load_chat_ids_from_file()

def add_user(user_id):
    if user_id not in users:
        users.add(user_id)
        save_chat_id_to_file(user_id)


def start(update, context):
    update.effective_message.reply_text(WELCOME_MESSAGE)

    user_info = update.effective_message.from_user.to_dict()

    context.bot.send_message(
        chat_id=TELEGRAM_SUPPORT_CHAT_ID,
        text=f"""
📞 Connected {user_info}.
        """,
    )


def forward_to_chat(update, context):
    """{ 
        'message_id': 5, 
        'date': 1605106546, 
        'chat': {'id': 49820636, 'type': 'private', 'username': 'danokhlopkov', 'first_name': 'Daniil', 'last_name': 'Okhlopkov'}, 
        'text': 'TEST QOO', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""
    forwarded = update.effective_message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)
    add_user(update.effective_message.from_user.id)
    if not forwarded.forward_from:
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            reply_to_message_id=forwarded.message_id,
            text=f'{update.effective_message.from_user.id}\n{REPLY_TO_THIS_MESSAGE}'
        )


def send_to_all(update, context):
    text = update.effective_message.text
    if text.startswith("/newsletter") == False:
        return
    #
    # message_to_send = text[len("/send_all "):]
    # recipients = []
    # for user_id in users:
    #     try:
    #         # context.bot.send_message(chat_id=user_id, text=message_to_send, photo=update.effective_message.photo)
    #         context.bot.copy_message(
    #             message_id=update.effective_message.message_id,
    #             chat_id=user_id,
    #             from_chat_id=update.effective_message.chat_id
    #         )
    #         recipients.append(user_id)
    #     except Exception as e:
    #         print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

    update.effective_message.reply_text(f"Reply for this message to send to all users")

# def send_to_all2(update, context):
#     text = update.effective_message.caption
#     if text.startswith("/send_all ") == False:
#         return
#
#     update.effective_message.caption = text[len("/send_all "):]
#     recipients = []
#     for user_id in users:
#         try:
#             # context.bot.send_message(chat_id=user_id, text=message_to_send, photo=update.effective_message.photo)
#             context.bot.copy_message(
#                 message_id=update.effective_message.message_id,
#                 chat_id=user_id,
#                 from_chat_id=update.effective_message.chat_id
#             )
#             recipients.append(user_id)
#         except Exception as e:
#             print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
#
#     update.effective_message.reply_text(f"Сообщение отправлено {len(recipients)} пользователям: {recipients}")


def forward_to_user(update, context):
    """{
        'message_id': 10, 'date': 1605106662, 
        'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True}, 
        'reply_to_message': {
            'message_id': 9, 'date': 1605106659, 
            'chat': {'id': -484179205, 'type': 'group', 'title': '☎️ SUPPORT CHAT', 'all_members_are_administrators': True}, 
            'forward_from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'danokhlopkov': 'okhlopkov', 'language_code': 'en'}, 
            'forward_date': 1605106658, 
            'text': 'g', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 
            'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 
            'from': {'id': 1440913096, 'first_name': 'SUPPORT', 'is_bot': True, 'username': 'lolkek'}
        }, 
        'text': 'ggg', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 
        'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""
    user_id = None
    if update.effective_message.reply_to_message.forward_from:
        user_id = update.effective_message.reply_to_message.forward_from.id
    elif REPLY_TO_THIS_MESSAGE in update.effective_message.reply_to_message.text:
        try:
            user_id = int(update.effective_message.reply_to_message.text.split('\n')[0])
        except ValueError:
            user_id = None
    if user_id:
        context.bot.copy_message(
            message_id=update.effective_message.message_id,
            chat_id=user_id,
            from_chat_id=update.effective_message.chat_id
        )
    else:
        # context.bot.send_message(
        #     chat_id=TELEGRAM_SUPPORT_CHAT_ID,
        #     text=WRONG_REPLY
        # )
        recipients = []
        for user_id in users:
            try:
                context.bot.copy_message(
                    message_id=update.effective_message.message_id,
                    chat_id=user_id,
                    from_chat_id=update.effective_message.chat_id
                )
                recipients.append(user_id)
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

        update.effective_message.reply_text(f"Сообщение отправлено {len(recipients)} пользователям: {recipients}")

def setup_dispatcher(dp):
    users_init()
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.chat_type.private, forward_to_chat))
    dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.reply, forward_to_user))
    dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.command, send_to_all))
    #dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.photo, send_to_all2))
    return dp
