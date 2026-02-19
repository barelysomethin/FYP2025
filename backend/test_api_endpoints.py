import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("HF_API_KEY")

endpoints = [
    "https://router.huggingface.co/models/facebook/bart-large-cnn",
    "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn",
    "https://router.huggingface.co/v1/models/facebook/bart-large-cnn",
    "https://router.huggingface.co/facebook/bart-large-cnn",
    "https://api-inference.huggingface.co/models/facebook/bart-large-cnn" 
]

headers = {"Authorization": f"Bearer {api_key}"}
payload = {"inputs": "This is a test sentence to summarize.", "parameters": {"min_length": 5}}

for url in endpoints:
    print(f"Testing {url}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)
