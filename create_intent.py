import requests
import json
import argparse

from google.cloud import dialogflow


def download_intent(url):
    try:
        intents_request = requests.get(url)
        intents_request.raise_for_status()
        intents = json.dumps(intents_request.json(), ensure_ascii=False)

        with open('intents.txt', 'w', encoding="utf-8") as my_file:
            my_file.write(intents)

    except Exception as e:
        print('Error', e)


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

    parser = argparse.ArgumentParser(description='По указаной ссылки с json-файлом добавляет запросы и ответы в GoogleFlow')
    parser.add_argument('--url', '-u', help='Укажите Url файла с запросами')
    args = parser.parse_args()
    download_intent(args)

    with open('intents.txt', 'r', encoding="utf-8") as my_file:
        file_content = my_file.read()

    intents = json.loads(file_content)

    for intent in intents.keys():
        display_name = intent
        training_phrases_parts = (intents.get(intent))['questions']
        message_texts = (intents.get(intent))['answer']
        create_intent('graphical-bus-431909-u0', display_name, training_phrases_parts, [message_texts])


if __name__ == '__main__':
    main()
