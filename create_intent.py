import requests
import json
import argparse

from environs import Env

from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    env = Env()
    env.read_env()

    g_project_id = env.str('GOOGLE_PROJECT_ID')

    parser = argparse.ArgumentParser(description='По указаной ссылки с json-файлом добавляет запросы и ответы в GoogleFlow')
    parser.add_argument('--url', '-u', help='Укажите Url файла с запросами')
    args = parser.parse_args()

    try:
        intents_request = requests.get(args.url)
        intents_request.raise_for_status()

        with open('intents.txt', 'r', encoding="utf-8") as file:
            file_content = file.read()

        intents = json.loads(file_content)

        for intent, responses in intents.items():
            display_name = intent
            training_phrases_parts = responses.get('questions')
            message_texts = responses.get('answer')
            create_intent(g_project_id, display_name, training_phrases_parts, [message_texts])

    except Exception as e:
        print('Error', e)


if __name__ == '__main__':
    main()
