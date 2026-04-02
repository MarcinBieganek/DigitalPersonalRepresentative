from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

class Agent:
    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def chat(self, message):
        messages = [{"role": "user", "content": message}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        
        return response.choices[0].message.content

