import logging

from environs import Env

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

env = Env()
env.read_env()

tg_token = env.str('TG_TOKEN')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


if __name__ == '__main__':

    updater = Updater(token=tg_token)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    updater.start_polling()

    updater.idle()
