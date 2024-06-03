import os

from groq import Groq

client = Groq(
    # api_key=os.environ.get("GROQ_API_KEY"),
    api_key="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"
)

def engine(query):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion

query = input("Enter your query: ")
# print(chat_completion.choices[0].message.content)
print(engine(query).choices[0].message.content)
