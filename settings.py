import os
from dotenv import load_dotenv, find_dotenv

# Loading .env variables
load_dotenv(find_dotenv())

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if TELEGRAM_TOKEN is None:
    raise Exception("Please setup the .env variable TELEGRAM_TOKEN.")

PORT = int(os.environ.get('PORT', '8443'))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")

TELEGRAM_SUPPORT_CHAT_ID = os.getenv("TELEGRAM_SUPPORT_CHAT_ID")
if TELEGRAM_SUPPORT_CHAT_ID is None or not str(TELEGRAM_SUPPORT_CHAT_ID).lstrip("-").isdigit():
    raise Exception("You need to specify 'TELEGRAM_SUPPORT_CHAT_ID' env variable: The bot will forward all messages to this chat_id. Add this bot https://t.me/ShowJsonBot to your private chat to find its chat_id.")
TELEGRAM_SUPPORT_CHAT_ID = int(TELEGRAM_SUPPORT_CHAT_ID)

CONNECTED_MESSAGE = os.getenv("CONNECTED_MESSAGE", "Connected!")
WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", "👋")
GET_NAME_MESSAGE = os.getenv("GET_NAME_MESSAGE", "What is your name?")
APPROVE_MESSAGE = os.getenv("APPROVE_MESSAGE", "Congratulations! You are approved!")
NAME_CHANGED_MESSAGE = os.getenv("NAME_CHANGED_MESSAGE", "Your name has been changed! New name:")
REPLY_TO_THIS_MESSAGE = os.getenv("REPLY_TO_THIS_MESSAGE", "REPLY_TO_THIS")
REPLY_TO_THIS_MESSAGE_FOR_ALL = os.getenv("REPLY_TO_THIS_MESSAGE_FOR_ALL", "REPLY_TO_THIS_MESSAGE_FOR_ALL")
WRONG_REPLY = os.getenv("WRONG_REPLY", "WRONG_REPLY")
WRONG_RENAME_MESSAGE = os.getenv("WRONG_RENAME_MESSAGE", "WRONG_RENAME_MESSAGE")