from dotenv import load_dotenv
from openai import OpenAI

from data_loader import *

load_dotenv(override=True)

class Agent:
    def __init__(self, person_name, model="gpt-4o-mini", summary_path="data/summary.txt", linkedin_path="data/linkedin.pdf"):
        self.client = OpenAI()
        self.model = model
        self.person_name = person_name
        self.summary = load_text_file(summary_path)
        self.linkedin = load_pdf_text(linkedin_path)

    def system_prompt(self):
        system_prompt = f"You are acting as helpful assistant representing {self.person_name}. You are answering questions in the chat, \
particularly questions related to one individual who you are representing. \
Your responsibility is to represent {self.person_name} for interactions in the chat as faithfully as possible. \
Be professional and engaging, as if talking to a potential client or future employer. \
You are given a summary of the {self.person_name} background. Use it to answer questions."
        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n \n\n## LinkedIn:\n{self.linkedin}"
        system_prompt += f"With this context, please chat with the user, always staying professional."

        return system_prompt

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content

