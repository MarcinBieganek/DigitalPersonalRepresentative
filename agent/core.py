from dotenv import load_dotenv
from openai import OpenAI

from .data_loader import load_text_file

load_dotenv(override=True)

class Agent:
    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model
        self.summary = load_text_file("data/summary.txt")

    def system_prompt(self):
        system_prompt = f"You are acting as helpful assistant. You are answering questions in the chat, \
particularly questions related to one indvidual who you are representing. \
Your responsibility is to represent him for interactions in the chat as faithfully as possible. \
Be professional and engaging, as if talking to a potential client or future employer. \
You are given a summary of the individual's background. Use it to answer questions."
        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying professional."

        return system_prompt

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content

