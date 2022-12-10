import os
import json
from sys import argv

import requests
from dotenv import load_dotenv

import openai

load_dotenv()
# Testing authorization
openai.organization = "org-VnHYjxm2msxII4nrKfrqCUQZ"
openai.api_key = os.getenv('API_KEY') 
openai.Model.list()

# Testing data fetch

prompt_text = argv[1]

url = "https://api.openai.com/v1/completions"
headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('API_KEY')}"
        }

data = {
            "model": "text-davinci-003",
            "prompt": f"Say {prompt_text}",
            "temperature": 0.7,
            "max_tokens": 20
        }

response = requests.post(url=url, headers=headers, json=data)
response_data = response.json()
response_message = response_data["choices"][0]["text"].replace("/n","")
print(response_message)

