from dotenv import load_dotenv
from openai import OpenAI
import json

from utils.data_loader import *
from agent.tools.factory import ToolFactory


load_dotenv(override=True)

class Agent:
    def __init__(self, person_name, model="gpt-4o-mini", summary_path="data/summary.txt", linkedin_path="data/linkedin.pdf", evaluator=None, max_reasks=3):
        self.client = OpenAI()
        self.model = model
        self.person_name = person_name
        self.summary = load_text_file(summary_path)
        self.linkedin = load_pdf_text(linkedin_path)
        self.evaluator = evaluator
        self.max_reasks = max_reasks

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
    
    def ask(self, messages, tools=None):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools or ToolFactory.tools_list()
        )

    def reask(self, reply, message, history, feedback):
        updated_system_prompt = self.system_prompt()
        updated_system_prompt += "\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
        updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
        updated_system_prompt += f"## Reason for rejection:\n{feedback}\n\n"
        messages = [{"role": "system", "content": updated_system_prompt}] + history + [{"role": "user", "content": message}]

        response = self.ask(messages)

        return response

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        needs_reask = False
        last_reply = None
        last_feedback = None
        reask_count = 0

        while True:
            if needs_reask:
                response = self.reask(last_reply, message, history, last_feedback)
                reask_count += 1
                # To avoid infinite loops:
                if reask_count > self.max_reasks:
                    return last_reply
            else:
                response = self.ask(messages)

            choice = response.choices[0]

            # Check if the model made a tool call
            if choice.finish_reason == "tool_calls":
                message_obj = choice.message
                tool_calls = message_obj.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message_obj)
                messages.extend(results)
                needs_reask = False
            # Check if response evalutaor is available
            elif self.evaluator:
                reply = choice.message.content
                evaluation = self.evaluator.evaluate(reply, message, history=messages)

                if hasattr(evaluation, 'is_acceptable') and not evaluation.is_acceptable:
                    needs_reask = True
                    last_reply = reply
                    last_feedback = evaluation.feedback if hasattr(evaluation, 'feedback') else "No feedback provided."
                else:
                    return reply
            # Respond without evaluation
            else:
                return choice.message.content