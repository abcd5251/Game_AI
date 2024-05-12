import tiktoken
import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_APIKEY")
client = OpenAI()

COMPLETIONS_MODEL = "gpt-3.5-turbo"

with open('action.yaml', 'r') as file:
    data = yaml.safe_load(file)

def num_tokens_from_string(string: str, encoding_name = COMPLETIONS_MODEL) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def generate_respond(question:str):
    goal_names = [goal['name'] for goal in data.get('goals', [])]
    intent_names = [intent['name'] for intent in data.get('intents', [])]

    input_messages = [
            {"role": "system", "content": f"You are a helpful assistant, given Categories below\n{goal_names}\nPlease classify user's input into one of the intent.Please output JSON."},
            {"role": "system", "content": "For example: ##User Input : I am ready for the game.\n##Output: {\"intent\": \"player_ready\"}"},                                                                                                                                                                                                                                  
            {"role": "user", "content": f"##User Input : {question}\n##Output: "}
        ]
    num_token = num_tokens_from_string(input_messages[0]["content"] + input_messages[1]["content"])
    print("total token spend for prompt :" ,num_token)
    
    response = client.chat.completions.create(
        model=COMPLETIONS_MODEL,
        messages=input_messages,
        response_format={ "type": "json_object" },
    )
    return response.choices[0].message.content


def speech_to_text(file_path : str):
    audio_file= open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )

    respond = generate_respond(transcription.text)
    return respond


