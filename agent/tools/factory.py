from agent.tools.record_user import RecordUserTool
from agent.tools.record_unknown import RecordUnknownTool

class ToolFactory:
    _tools = {
        "record_user_details": RecordUserTool,
        "record_unknown_question": RecordUnknownTool,
    }

    @classmethod
    def get_tool(cls, name):
        tool_cls = cls._tools.get(name)
        if not tool_cls:
            raise ValueError(f"Tool '{name}' not found.")
        return tool_cls()

    @classmethod
    def tools_list(cls):
        return [
            {"type": "function", "function": tool().json_schema}
            for tool in cls._tools.values()
        ]
