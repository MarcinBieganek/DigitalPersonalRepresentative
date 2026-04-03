
def record_unknown_question(question):
    print("Unknown question:", question)
    return {"status": "ok"}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Record unknown questions",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string"}
        },
        "required": ["question"]
    }
}

tools_list = [
    {"type": "function", "function": record_unknown_question_json}
]
