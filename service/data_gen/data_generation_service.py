import os
import re
from json import dumps
from typing import Any, List

from ftfy import fix_text
from text_unidecode import unidecode

from models.conversation_turn import ConversationTurn
from models.http.request.data.data_generation_request import DataGenerationRequest
from service.data_gen.base.base_data_service import BaseDataService
from service.data_gen.base.story_data_service import StoryDataService
from service.data_gen.data.conversation_data_service import ConversationDataService
from service.data_gen.data.fact_data_service import FactDataService
from service.data_gen.data.habit_data_service import HabitDataService
from service.data_gen.data.hobby_data_service import HobbyDataService
from service.data_gen.data.introspection_data_service import IntrospectionDataService
from service.data_gen.data.like_data_service import LikeDataService
from service.data_gen.data.memory_data_service import MemoryDataService
from service.data_gen.data.monologue_data_service import MonologueDataService
from service.data_gen.data.relationship_data_service import RelationshipDataService
from service.data_gen.data.self_description_data_service import SelfDescriptionDataService
from service.data_gen.data.speech_data_service import SpeechDataService
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.reasoning_conversation_service import ReasoningConversationService
from service.persona_domain.story_service import StoryService

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
class DataGenerationService:
    def __init__(self,
                 persona_service: PersonaService,
                 story_service: StoryService,
                 speech_data_service: SpeechDataService,
                 conversation_data_service: ConversationDataService,
                 story_data_service: StoryDataService,
                 relationship_data_service: RelationshipDataService,
                 memory_data_service: MemoryDataService,
                 like_data_service: LikeDataService,
                 introspection_data_service: IntrospectionDataService,
                 base_data_service: BaseDataService,
                 reasoning_service: ReasoningConversationService,
                 habit_data_service: HabitDataService,
                 monologue_data_service: MonologueDataService,
                 hobby_data_service: HobbyDataService,
                 self_description_conversation_data_service: SelfDescriptionDataService,
                 fact_data_service: FactDataService,
                 ):
        self.persona_service = persona_service
        self.conversation_data_service = conversation_data_service
        self.speech_data_service = speech_data_service
        self.story_data_service = story_data_service
        self.relationship_data_service = relationship_data_service
        self.memory_data_service = memory_data_service
        self.like_data_service = like_data_service
        self.story_service = story_service
        self.introspection_data_service = introspection_data_service
        self.base_data_service = base_data_service
        self.reasoning_service = reasoning_service
        self.habit_data_service = habit_data_service
        self.monologue_data_service = monologue_data_service
        self.hobby_data_service = hobby_data_service
        self.self_description_conversation_data_service = self_description_conversation_data_service
        self.fact_data_service = fact_data_service

    def generate(self, universe_id: int, data_gen_request: DataGenerationRequest) -> dict[Any, Any]:
        for f in os.listdir("stuff/data"):
            os.remove(os.path.join("stuff/data", f))
        result = {}
        personas = [self.persona_service.find_by_id(persona.id) for persona in data_gen_request.personas] if len(data_gen_request.personas) > 0 else self.persona_service.find_by_universe(universe_id)
        for persona in personas:
            persona_data = {'likes': self.like_data_service.generate(persona_id=persona.id),
                            'habits': self.habit_data_service.generate(persona_id=persona.id),
                            'speech': self.speech_data_service.generate(persona_id=persona.id),
                            'relationship': self.relationship_data_service.generate(persona_id=persona.id),
                            'introspection': self.introspection_data_service.generate(persona_id=persona.id),
                            'memory': self.memory_data_service.generate(persona_id=persona.id),
                            'conversation': self.conversation_data_service.generate(persona_id=persona.id),
                            'monologue': self.monologue_data_service.generate(persona_id=persona.id),
                            'casual_conversation': self.self_description_conversation_data_service.generate(persona_id=persona.id),
                            'facts': self.fact_data_service.generate(persona_id=persona.id)}
            result[persona.backstory.name] = persona_data
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
                                    intent = self.update_names(intent, turn.speaker, personas)
                                    new_turn["intent"] = intent
                                if turn.private_thought is not None:
                                    thought = turn.private_thought
                                    thought = self.update_names(thought, turn.speaker, personas)
                                    new_turn["thought"] = thought
                                if turn.feeling is not None:
                                    new_turn["emotion"] = turn.feeling
                                if turn.action is not None:
                                    action = turn.action
                                    action = self.update_names(action, turn.speaker, personas)
                                    new_turn["action"] = action
                                if turn.tone is not None:
                                    new_turn["tone"] = turn.tone
                                if turn.text is not None:
                                    text = turn.text
                                    text = fix_text(text)
                                    text = unidecode(text)

                                    for math_key in MATH_MAP:
                                        text = text.replace(math_key, MATH_MAP[math_key])
                                    text = self.update_names(text=text, speaker=turn.speaker, personas=personas)
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
        print("completed")
        return result


    def update_names(self, text, speaker, personas):
        text = text.replace(speaker, "I")
        text = re.sub(r"{" + speaker + "'s+}", f"{speaker}", text)
        text = re.sub(" (\\[a-zA-Z])", "\\\1", text)
        text = re.sub("(\$\\[a-zA-Z])", "\\\1", text)
        text = re.sub("\time", "\\time", text)
        text = re.sub("ladies and gentlemen,", "", text)
        return text