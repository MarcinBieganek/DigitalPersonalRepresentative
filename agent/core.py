from dotenv import load_dotenv
from openai import OpenAI
import json

from utils.data_loader import *
from agent.tools.factory import ToolFactory


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
    
    def handle_tool_call(self, tool_calls):
        results = []
        for call in tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments)

            print(f"Tool called: {name}", flush=True)
            try:
                tool = ToolFactory.get_tool(name)
                result = tool.run(**args)
            except Exception as e:
                result = {"error": f"Exception in tool '{name}': {str(e)}"}

            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": call.id
            })

        return results


    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]

        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=ToolFactory.tools_list()
            )
            choice = response.choices[0]

            if choice.finish_reason == "tool_calls":
                message = choice.message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                return choice.message.content