from ollama import chat

response = chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "user",
            "content": "Say only: Hello World"
        }
    ],
)

print(response.message.content)