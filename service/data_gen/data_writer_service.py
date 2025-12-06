import re
from json import dumps
from typing import List

from ftfy import fix_text
from text_unidecode import unidecode

from models.conversation_turn import ConversationTurn

MATH_MAP = {
    "²": r"\^2",
    "ℝ": r"\mathbb{R}",
    "ℤ": r"\mathbb{Z}",
    "ℚ": r"\mathbb{Q}",
    "ℕ": r"\mathbb{N}",
    "∞": r"\infty",
    "∑": r"\sum",
    "∏": r"\prod",
    "∫": r"\int",
    "→": r"\to",
    "≤": r"\leq",
    "≥": r"\geq",
    "≠": r"\neq",
    "≈": r"\approx"
}
class DataWriterService:
    def update_names(self, text, speaker):
        text = text.replace(speaker, "I")
        text = re.sub(" (\\[a-zA-Z])", "\\\1", text)
        text = re.sub("(\$\\[a-zA-Z])", "\\\1", text)
        text = re.sub("\time", "\\time", text)
        text = re.sub("ladies and gentlemen,", "", text)
        return text

    def write_data(self, data):
        for persona_data in data.values():
            for key in persona_data:
                with open(f"stuff/data/{key}.jsonl", "a+", encoding="utf-8") as f:
                    for conversation in persona_data[key]:
                        if conversation.conversation_turns is not None:
                            turns: List[ConversationTurn] = conversation.conversation_turns
                            conversation_turns = []
                            for i, turn in enumerate(turns):
                                new_turn = {}
                                new_turn["speaker"] = turn.speaker
                                if turn.directed_at is not None:
                                    directed_at = turn.directed_at
                                    if directed_at == [] or directed_at == ["audience"]:
                                        directed_at = ["everyone"]
                                    new_turn["speaking to"] = directed_at
                                if turn.turn_intent is not None:
                                    intent = turn.turn_intent
                                    intent = self.update_names(intent, turn.speaker)
                                    new_turn["intent"] = intent
                                if turn.private_thought is not None:
                                    thought = turn.private_thought
                                    thought = self.update_names(thought, turn.speaker)
                                    new_turn["thought"] = thought
                                if turn.feeling is not None:
                                    new_turn["emotion"] = turn.feeling
                                if turn.action is not None:
                                    action = turn.action
                                    action = self.update_names(action, turn.speaker)
                                    new_turn["action"] = action
                                if turn.tone is not None:
                                    new_turn["tone"] = turn.tone
                                if turn.text is not None:
                                    text = turn.text
                                    text = fix_text(text)
                                    text = unidecode(text)

                                    for math_key in MATH_MAP:
                                        text = text.replace(math_key, MATH_MAP[math_key])
                                    text = self.update_names(text=text, speaker=turn.speaker)
                                    new_turn["speech"] = text
                                conversation_turns.append(new_turn)
                            conversation_json = dumps(conversation_turns, ensure_ascii=False)
                            conversation_json = conversation_json.replace("[{", "[ {")
                            conversation_json = conversation_json.replace("\":", "\" :")
                            conversation_json = conversation_json.replace("{\"", "{ \"")
                            conversation_json = conversation_json.replace("]}", "] }")
                            conversation_json = conversation_json.replace("\",", "\" ,")
                            conversation_json = conversation_json.replace("},", "} ,")
                            conversation_json = conversation_json.replace("}]", "} ]")
                            conversation_json = conversation_json.replace("[\"", "[ \"")
                            conversation_json = conversation_json.replace("\"]", "\" ]")
                            if len(conversation.conversation_turns) > 0:
                                f.write(f"{conversation_json}\n")