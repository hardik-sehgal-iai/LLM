from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()


response = client.chat.completions.create(
    model="gpt-4", 
    messages=[
        {"role": "user", "content": "Hey there"} # zero shot prompting
    ]
)

print(response.choices[0].message.content)