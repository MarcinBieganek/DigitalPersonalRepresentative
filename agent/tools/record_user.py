from agent.tools.base import Tool
from utils.push import push

class RecordUserTool(Tool):
    @property
    def json_schema(self):
        return {
            "name": "record_user_details",
            "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "The email address of this user"},
                    "name": {"type": "string", "description": "The user's name, if they provided it"},
                    "notes": {"type": "string", "description": "Any additional information about the conversation that's worth recording to give context"}
                },
                "required": ["email"],
                "additionalProperties": False
            }
        }

    def run(self, email, name="Name not provided", notes="not provided"):
        push(f"Recording {name} with email {email} and notes {notes}")
        return {"recorded": "ok"}
