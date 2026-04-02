from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

class Agent:
    def __init__(self):
        self.client = OpenAI()
