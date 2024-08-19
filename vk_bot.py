import logging
import requests
import time
import vk_api
import random

from functools import partial
from get_intents import vk_detect_intent_texts
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env

logger = logging.getLogger("Debug")


def get_response(g_project_id, event, vk_api):
    vk_api.messages.send(user_id=event.user_id,
                         message=vk_detect_intent_texts(g_project_id, event.user_id, event.text, 'en-US'),
                         random_id=random.randint(1, 1000)
    )


def main():

    env = Env()
    env.read_env()

    vk_token = env.str('VK_TOKEN')
    vk_session = vk_api.VkApi(token=vk_token)
    longpoll = VkLongPoll(vk_session)

    g_project_id = env.str('GOOGLE_PROJECT_ID')
    bot_talk = partial(get_response, g_project_id)
    vk_api_session = vk_session.get_api()

    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    bot_talk(event, vk_api_session)
        except Exception as e:
            print('Error', e)
            time.sleep(60)
        except requests.ConnectionError:
            time.sleep(30)


if __name__ == "__main__":
    main()