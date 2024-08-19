import logging
import requests
import time

from environs import Env

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from get_intents import tg_detect_intent_texts


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def talk(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        tg_detect_intent_texts(g_project_id, update.effective_user.id, update.message.text, 'en-US')
    )


if __name__ == '__main__':

    env = Env()
    env.read_env()

    tg_token = env.str('TG_TOKEN')
    g_project_id = env.str('GOOGLE_PROJECT_ID')
    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    while True:
        try:
            start_handler = CommandHandler('start', start)

            dispatcher.add_handler(CommandHandler("start", start))
            dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), talk))

            updater.start_polling()
            updater.idle()

        except Exception as e:
            print('Error', e)
            time.sleep(60)
        except requests.ConnectionError:
            time.sleep(30)
