import os
import json
from dotenv import load_dotenv
from openai_client import get_openai_embeddings

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

INPUT_DIR = './data/input'
OUTPUT_DIR = './data/embeddings'

for filename in os.listdir(INPUT_DIR):
    if filename.endswith('.json'):
        file_path = os.path.join(INPUT_DIR, filename)
        with open(file_path, 'r') as f:
            print("fetching embeddings for " + file_path)

            data = json.load(f)
            description = data['description']
            result = get_openai_embeddings(description, OPENAI_API_KEY)
            data["openai_embeddings"] = result

            with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
