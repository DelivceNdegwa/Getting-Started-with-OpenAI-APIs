import os
import json
from sys import argv

import requests
from dotenv import load_dotenv

import openai
from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3


load_dotenv()
# Testing authorization
openai.organization = os.getenv('ORGANIZATION_KEY')
openai.api_key = os.getenv('API_KEY') 
openai.Model.list()

# Testing data fetch

interaction_type = argv[1].lower()
# print(interaction_type)

def open_ai_completions_request(prompt_text):
    url = "https://api.openai.com/v1/completions"
    headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.getenv('API_KEY')}"
            }

    data = {
                "model": "text-davinci-003",
                "prompt": f"Say {prompt_text}",
                "temperature": 0.7,
                "max_tokens": 500
            }

    response = requests.post(url=url, headers=headers, json=data)
    response_data = response.json()
    response_message = response_data["choices"][0]["text"].replace("/n","")
    
    return response_message

def text_to_speech(input_text):
    # init function to get an engine instance for the speech synthesis
    engine = pyttsx3.init()
    speech_rate = engine.getProperty("rate")
    
    engine.setProperty("rate", speech_rate-15)
    engine.setProperty("voice", "english-us")
    
    # say method on the engine that passing input text to be spoken
    engine.say(input_text)
    
    # run and wait method, it processes the voice commands.
    engine.runAndWait()

def text_communication():
    message = input("Your input: ")
    print(open_ai_completions_request(message))
    text_communication()

def speech_communication():
    model = Model("vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    while True:
        data = stream.read(4096)

        if recognizer.AcceptWaveform(data):
            text = json.loads(recognizer.Result()).get("text")
            print(f"Speech text: {text}")
            response = open_ai_completions_request(text)
            if response:
                text_to_speech(response)
                print(response)
                speech_communication()
            

if interaction_type == "text":
    text_communication()
elif interaction_type == "speech":
    speech_communication()          

else:
    print("Choose either speech or text")
    
