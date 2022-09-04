import requests

API_URL = (
    "https://api-inference.huggingface.co/models/bhadresh-savani/bert-base-go-emotion"
)
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
