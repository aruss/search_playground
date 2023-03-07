import requests


def get_openai_embeddings(input_text, api_key):
    url = 'https://api.openai.com/v1/embeddings'
    headers = {'Authorization': 'Bearer ' + api_key}
    data = {"input": input_text, "model": "text-embedding-ada-002"}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Error:', response.status_code, response.text)
