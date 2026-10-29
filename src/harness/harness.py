import sys
import requests
import json

BASE_URL = "http://example.com:1234/v1"
MODEL_NAME = "example_model"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a file given its path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the file to read."
                    }
                },
                "required": ["path"]
            }
        }
    }
]

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def call_tool(tool_call):
    if tool_call["name"] == "read_file":
        path = json.loads(tool_call["arguments"])["path"]
        contents = read_file(path)
        return json.dumps({
            "tool_name": "read_file",
            "path": path,
            "contents": contents,
            "success": True
        })
    return ""

def call_api(model, messages, tools):
    response = requests.post(f"{BASE_URL}/chat/completions",
                             json={
                                 "model": model,
                                 "messages": messages,
                                 "tools": tools,
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

        while True:
            choice = call_api(model=MODEL_NAME, messages=messages, tools=TOOLS)

            message = choice["message"]
            messages.append(message)

            if message.get("reasoning_content", "").strip() != "":
                print("Reasoning Content: ", message["reasoning_content"])
                print()

            if choice["finish_reason"] != "tool_calls":
                print("Content: ", message["content"])
                print()
                break

            for tool_call in message["tool_calls"]:
                print("Tool call:", tool_call["function"]["name"])
                print()

                result = call_tool(tool_call["function"])
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": result
                })