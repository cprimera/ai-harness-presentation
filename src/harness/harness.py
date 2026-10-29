import sys
import requests


BASE_URL = "http://example.com:1234/v1"
MODEL_NAME = "example_model"

def call_api(model, messages):
    response = requests.post(f"{BASE_URL}/chat/completions",
                             json={
                                 "model": model,
                                 "messages": messages,
                             })
    choice = response.json()["choices"][0]
    return choice

def main() -> None:
    if sys.argv[1:]:
        prompt = " ".join(sys.argv[1:])
        print("Prompt: ", prompt)
        print()

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]

        choice = call_api(model=MODEL_NAME, messages=messages)

        message = choice["message"]

        if message.get("reasoning_content", "").strip() != "":
            print("Reasoning Content: ", message["reasoning_content"])
            print()

        if message.get("content", "").strip() != "":
            print("Content: ", message["content"])
            print()