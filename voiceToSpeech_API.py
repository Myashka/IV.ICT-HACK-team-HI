import json
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"
headers = {"Authorization": "Bearer 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"}

def query(data):
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))