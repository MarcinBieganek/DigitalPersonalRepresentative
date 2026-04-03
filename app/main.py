import gradio 
from agent.core import Agent

agent = Agent("John")

def chat_fn(message, history):
    return agent.chat(message, history)

gradio.ChatInterface(chat_fn).launch()
