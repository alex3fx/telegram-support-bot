from telegram.ext import Updater

from handlers import setup_dispatcher
from settings import TELEGRAM_TOKEN, HEROKU_APP_NAME, PORT
import time

# Setup bot handlers
updater = Updater(TELEGRAM_TOKEN, )

dp = updater.dispatcher
dp = setup_dispatcher(dp)

# Run bot
while True:
    try:
        if HEROKU_APP_NAME is None:  # pooling mode
            print("Can't detect 'HEROKU_APP_NAME' env. Running bot in pooling mode.")
            print("Note: this is not a great way to deploy the bot in Heroku.")

            updater.start_polling()
            updater.idle()

        else:  # webhook mode
            print(
                f"Running bot in webhook mode. Make sure that this url is correct: https://{HEROKU_APP_NAME}.herokuapp.com/")
            updater.start_webhook(
                listen="0.0.0.0",
                port=PORT,
                url_path=TELEGRAM_TOKEN,
                webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TELEGRAM_TOKEN}"
            )

            updater.idle()
    except Exception as e:
        print(f"Error occurred: {e.message}. Retrying in 60 seconds.")
        time.sleep(60)

