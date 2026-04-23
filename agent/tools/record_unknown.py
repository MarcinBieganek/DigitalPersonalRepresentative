from agent.tools.base import Tool
from utils.push import push

class RecordUnknownTool(Tool):
    @property
    def json_schema(self):
        return {
            "name": "record_unknown_question",
            "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The question that couldn't be answered"}
                },
                "required": ["question"],
                "additionalProperties": False
            }
        }

    def run(self, question):
        push(f"Recording {question}")
        return {"recorded": "ok"}
