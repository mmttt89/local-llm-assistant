import requests

response = requests.post(
    "http://localhost:1234/v1/chat/completions",
    json={
        "messages": [
            {
                "role": "user",
                "content": "Explain React Native Hooks"
            }
        ]
    }
)

print(response.json())