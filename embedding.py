import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

input = sys.argv[1]
url = 'https://api.openai.com/v1/embeddings'
headers = {'Authorization': 'Bearer ' + OPENAI_API_KEY}
data = {"input": input, "model": "text-embedding-ada-002"}

response = requests.post(url, json=data, headers=headers)
print(response.json())
