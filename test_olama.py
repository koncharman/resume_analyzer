
import ollama

response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": "Give me 5 skills for an AI engineer, short answer"
        }
    ]
)

print(response["message"]["content"])