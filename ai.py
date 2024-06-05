from openai import OpenAI

client = OpenAI(
    api_key='sk-proj-CHeuBjBrmddwJL0OIQUbT3BlbkFJk9iEfpvcxcewlfd30SeI' #cheia API trebuie platita
)

prompt="Which country is the most beautiful?"
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role":"user",
            "content":prompt
        }
    ],
    model="gpt-3.5-turbo"
)
print(chat_completion)