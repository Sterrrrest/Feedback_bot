import requests
import json

from google.cloud import dialogflow

url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'


def download_intent(url):

    intents_request = requests.get(url)
    intents_request.raise_for_status()
    intents = json.dumps(intents_request.json(), ensure_ascii=False)

    with open('intents.txt', 'w', encoding="utf-8") as my_file:
        my_file.write(intents)
    # t = json.loads(intents)


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


def list_intents(project_id):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)

    intents = intents_client.list_intents(request={"parent": parent})

    for intent in intents:
        print("=" * 20)
        print("Intent name: {}".format(intent.name))
        print("Intent display_name: {}".format(intent.display_name))
        print("Action: {}\n".format(intent.action))
        print("Root followup intent: {}".format(intent.root_followup_intent_name))
        print("Parent followup intent: {}\n".format(intent.parent_followup_intent_name))

        print("Input contexts:")
        for input_context_name in intent.input_context_names:
            print("\tName: {}".format(input_context_name))

        print("Output contexts:")
        for output_context in intent.output_contexts:
            print("\tName: {}".format(output_context.name))


def main():

    # list_intents('graphical-bus-431909-u0')
    # download_intent(url)

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
