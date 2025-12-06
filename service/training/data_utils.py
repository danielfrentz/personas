
datasets = {
    "likes": lambda: get_persona_data("likes.jsonl"),
    "habits": lambda: get_persona_data("habits.jsonl"),
    "monologue": lambda: get_persona_data("monologue.jsonl"),
    "conversation": lambda: get_persona_data("conversation.jsonl"),
    "introspection": lambda: get_persona_data("introspection.jsonl"),
    "memory": lambda: get_persona_data("memory.jsonl"),
    "relationship": lambda: get_persona_data("relationship.jsonl"),
    "speech": lambda: get_persona_data("speech.jsonl"),
    "facts": lambda: get_persona_data("facts.jsonl"),
    "base": lambda: get_base_data(),
    "maths": lambda: get_maths_data(),
    "turns": lambda: get_turns()
}


def get_dataset(names):
    return sum([datasets[name]() for name in names], [])