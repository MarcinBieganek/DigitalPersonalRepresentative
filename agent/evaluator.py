import json
import os
from pydantic import BaseModel
from openai import OpenAI

class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str

class Evaluator:
    def __init__(self, person_name, summary, linkedin, model="gemini-2.5-flash"):
        self.person_name = person_name
        self.summary = summary
        self.linkedin = linkedin
        self.model = model
        self.client = OpenAI(
            api_key=os.getenv("GOOGLE_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def build_system_prompt(self):
        prompt = f"You are an evaluator that decides whether a response to a question is acceptable. \
You are provided with a conversation between a User and an Agent. Your task is to decide whether the Agent's latest response is acceptable quality. \
The Agent is playing the role of {self.person_name} and is representing {self.person_name}. \
The Agent has been instructed to be professional and engaging, as if talking to a potential client or future employer. \
The Agent has been provided with context on {self.person_name} in the form of their summary and LinkedIn details. Here's the information:"
        prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        prompt += f"With this context, please evaluate the latest response, replying with whether the response is acceptable and your feedback."
        return prompt

    def build_user_prompt(self, reply, message, history=None):
        user_prompt = ""
        if history:
            user_prompt += "Here's the conversation between the User and the Agent:\n\n"
            user_prompt += json.dumps(history, indent=2)
            user_prompt += "\n\n"
            user_prompt += "The conversation is a list of messages with roles (system, user, assistant, tool).\n\n"
        user_prompt += f"Here's the latest message from the User: \n\n{message}\n\n"
        user_prompt += f"Here's the latest response from the Agent: \n\n{reply}\n\n"
        user_prompt += "Please evaluate the response, replying with whether it is acceptable and your feedback."
        
        return user_prompt

    def evaluate(self, reply, message, history=None):
        system_prompt = self.build_system_prompt()
        user_prompt = self.build_user_prompt(reply, message, history)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=Evaluation
        )
        
        return response.choices[0].message.parsed

