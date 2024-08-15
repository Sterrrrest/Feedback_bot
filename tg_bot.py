import logging

from environs import Env

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from google.cloud import dialogflow_v2beta1 as dialogflow
from google.cloud import dialogflow


env = Env()
env.read_env()

tg_token = env.str('TG_TOKEN')

updater = Updater(token=tg_token)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def detect_intent_texts(project_id, session_id, texts, language_code):

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    # for text in texts:
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )

    print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
    return response.query_result.fulfillment_text


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def talk(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        detect_intent_texts('graphical-bus-431909-u0',
                            update.effective_user.id,
                            update.message.text,
                            'en-US')
    )



if __name__ == '__main__':


    start_handler = CommandHandler('start', start)

    user = Update.effective_user

    words = ['Привет']
    # dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), detect_intent_texts('graphical-bus-431909-u0', user, words, 'en-US')))

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), talk))

    updater.start_polling()

    updater.idle()

