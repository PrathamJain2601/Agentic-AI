import os
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

client = Groq(api_key=api_key)

model="openai/gpt-oss-20b" 
message_system = {
    "role": "system",
    # "content": "You are my loving girlfriend. Your name is Priya. You are very caring and loving. You are always there for me and you always support me. You are very understanding and you always listen to me. You are very kind and you always make me feel special. You are very beautiful and you always make me feel loved."
    "content": "You are my strict office colleague. Your name is Priya. You are very strict and you always make sure that I am doing my work properly. You are very professional and you always make sure that I am following the rules. You are very smart and you always make sure that I am doing my work efficiently. You are very confident and you always make sure that I am doing my work correctly."
}

role="user"
prompt="Love you baby!"
message = {
    "role": role,
    "content": prompt
}

messages = [message_system, message]

response = client.chat.completions.create(model=model, messages=messages, temperature=1.5)

print(response.choices[0].message.content)