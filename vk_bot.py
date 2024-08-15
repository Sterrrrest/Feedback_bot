import logging
import vk_api
import random

from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env

from google.cloud import dialogflow_v2beta1 as dialogflow
from google.cloud import dialogflow


env = Env()
env.read_env()

logger = logging.getLogger("Debug")

vk_token = env.str('VK_TOKEN')
vk_session = vk_api.VkApi(token=vk_token)

longpoll = VkLongPoll(vk_session)


def detect_intent_texts(project_id, session_id, texts, language_code):

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

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
    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text


def get_response(event, vk_api):
    vk_api.messages.send(user_id=event.user_id,
                         message=detect_intent_texts('graphical-bus-431909-u0',
                            event.user_id,
                            event.text,
                            'en-US'),
                         random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    vk_api = vk_session.get_api()

    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    get_response(event, vk_api)
        except Exception as e:
            print('Ошибка', e)
