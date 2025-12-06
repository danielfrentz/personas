import logging
from typing import List

from models.conversation import Conversation
from models.conversation_turn import ConversationTurn
from service.persona_domain.memory_service import MemoryService
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.story_service import StoryService

recall_phrases = [
    "I'm trying to recall details about {event_title}",
    "Recalling details about {event_title}",
    "I'm trying to recall a past experience, in particular regarding {event_title}",
    "Recalling a past experience, around the time of {event_title}",
    "I remember {event_title} well..."
]

class MemoryDataService:
    memory_text = "{memory_text}. this happened during {story_title}. remembering it makes me feel {feelings_stirred}"
    def __init__(self, story_service: StoryService, memory_service: MemoryService, persona_service: PersonaService):
        self.story_service = story_service
        self.memory_service = memory_service
        self.persona_service = persona_service
        self.logger = logging.getLogger(__name__)

    def generate(self, persona_id: int) -> List[Conversation]:
        result = []
        persona = self.persona_service.find_by_id(persona_id)
        for event in persona.life_events:
            if event.story and event.story.memories:
                for idx, memory in enumerate(event.story.memories):
                    try:
                        talking_self_query = ConversationTurn(
                            turn_intent="Recalling a past experience",
                            directed_at=[f"{persona.backstory.name}'s memory"],
                            speaker=f"{persona.backstory.name}",
                            text=recall_phrases[idx].format(event_title=event.story.title),
                            action=f"Recalling a past experience",
                            tone="thoughtful",
                            feeling=memory.feelings_stirred
                        )
                        talking_self_memory = ConversationTurn(
                            directed_at=[persona.backstory.name],
                            speaker=f"{persona.backstory.name}'s memory",
                            text=memory.memory_text.format(memory_title=memory.story_title, feelings_stirred=memory.feelings_stirred, memory_text=memory.memory_text),
                            action=f"Remembering my past experience",
                            tone="thoughtful",
                            feeling=memory.feelings_stirred
                        )

                        result.append(Conversation(conversation_turns=[talking_self_query, talking_self_memory]))

                        reflex_turn = ConversationTurn(
                            directed_at=[persona.backstory.name],
                            turn_intent="Recalling a memory related to my current task",
                            speaker=persona.backstory.name,
                            text=memory.memory_reflex,
                            action=f"Remembering my past experience",
                            tone="thoughtful",
                            feeling=memory.feelings_stirred
                        )
                        reflex_action_turn = ConversationTurn(
                            turn_intent="Speaking to the crowd",
                            directed_at=[persona.backstory.name],
                            speaker=persona.backstory.name,
                            text=memory.memory_reflex_followup,
                            feeling=memory.feelings_stirred,
                            action=f"Using what I recalled to speak to the crowd",
                            tone="powerful"
                        )
                        result.append(Conversation(conversation_turns=[reflex_turn, reflex_action_turn]))
                    except Exception as e:
                        self.logger.info(f"could not write memory {memory.memory_text}")
        logging.info(f"returning {len(result)} memories")
        return result
