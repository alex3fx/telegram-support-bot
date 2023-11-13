import json
from telegram.ext import CommandHandler, MessageHandler, Filters

from settings import (WELCOME_MESSAGE, TELEGRAM_SUPPORT_CHAT_ID, REPLY_TO_THIS_MESSAGE, WRONG_REPLY,
                      GET_NAME_MESSAGE, APPROVE_MESSAGE, NAME_CHANGED_MESSAGE, WRONG_RENAME_MESSAGE,
                      CONNECTED_MESSAGE, REPLY_TO_THIS_MESSAGE_FOR_ALL)

users = {}  # Простое хранилище chat_id пользователей. В реальном приложении лучше использовать БД.

def users_init():
    global users
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
            return
    except FileNotFoundError:
        print("users.json not found")
        pass



def save_users():
    global users
    with open("users.json", "w") as file:
        json.dump(users, file)



def add_edit_user(user_id, name=None, tag=None):
    global users
    str_id = str(user_id)
    if str_id not in users:
        users[str_id] = {
            "name": name,
            "tag": tag
        }
    else:
        if name:
            users[str_id]["name"] = name
        if tag and users[str_id]["tag"] is None:
            users[str_id]["tag"] = tag

    save_users()


def get_user(user_id):
    global users
    str_id = str(user_id)
    if str_id not in users:
        return {}
    return users[str_id]

def start(update, context):
    update.effective_message.reply_text(WELCOME_MESSAGE)

    user_info = update.effective_message.from_user.to_dict()

    user = get_user(update.effective_message.from_user.id)
    if  user == {}:
        add_edit_user(update.effective_message.from_user.id)
        update.effective_message.reply_text(GET_NAME_MESSAGE)

        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            text=f"""{CONNECTED_MESSAGE} {user_info}. """,
        )

def rename(update, context):
    if get_user(update.effective_message.from_user.id)["name"] is None:
        add_edit_user(update.effective_message.from_user.id)
        update.effective_message.reply_text(GET_NAME_MESSAGE)
        return


    text = update.effective_message.text[len("/rename "):]
    names = text.split()
    if len(names) != 2:
        update.effective_message.reply_text(WRONG_RENAME_MESSAGE)
        return

    add_edit_user(update.effective_message.from_user.id, name=text, tag="#"+''.join(names).lower())
    update.effective_message.reply_text(NAME_CHANGED_MESSAGE + " " + text)
    return



def forward_to_chat(update, context):
    """{ 
        'message_id': 5, 
        'date': 1605106546, 
        'chat': {'id': 49820636, 'type': 'private', 'username': 'danokhlopkov', 'first_name': 'Daniil', 'last_name': 'Okhlopkov'}, 
        'text': 'TEST QOO', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 
        'from': {'id': 49820636, 'first_name': 'Daniil', 'is_bot': False, 'last_name': 'Okhlopkov', 'username': 'danokhlopkov', 'language_code': 'en'}
    }"""

    user = get_user(update.effective_message.from_user.id)
    if  user == {}:
        add_edit_user(update.effective_message.from_user.id)
        update.effective_message.reply_text(GET_NAME_MESSAGE)
        return

    if user["name"] is None:
        names = update.effective_message.text.split()
        if len(names) != 2:
            update.effective_message.reply_text(GET_NAME_MESSAGE)
            return
        add_edit_user(update.effective_message.from_user.id, name=update.effective_message.text, tag="#"+''.join(names).lower())
        update.effective_message.reply_text(APPROVE_MESSAGE)
        return

    # context.bot.send_message(chat_id=TELEGRAM_SUPPORT_CHAT_ID, text=user["name"] + " " + user["tag"])
    forwarded = update.effective_message.forward(chat_id=TELEGRAM_SUPPORT_CHAT_ID)

    if not forwarded.forward_from:
        context.bot.send_message(
            chat_id=TELEGRAM_SUPPORT_CHAT_ID,
            reply_to_message_id=forwarded.message_id,
            text=f'{update.effective_message.from_user.id}\n{REPLY_TO_THIS_MESSAGE}'
        )


def send_to_all(update, context):
    text = update.effective_message.text
    if text.startswith("/newsletter"):
        update.effective_message.reply_text(REPLY_TO_THIS_MESSAGE_FOR_ALL)



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
        if REPLY_TO_THIS_MESSAGE_FOR_ALL != update.effective_message.reply_to_message.text:
            context.bot.send_message(
                chat_id=TELEGRAM_SUPPORT_CHAT_ID,
                text=WRONG_REPLY
            )
            return

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
    dp.add_handler(CommandHandler('rename', rename))
    dp.add_handler(MessageHandler(Filters.chat_type.private, forward_to_chat))
    dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.reply, forward_to_user))
    dp.add_handler(MessageHandler(Filters.chat(TELEGRAM_SUPPORT_CHAT_ID) & Filters.command, send_to_all))
    #dp.add_handler(MessageHandler(Filters.command, send_to_all2))
    return dp
