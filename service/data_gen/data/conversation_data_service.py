import logging
from typing import List

from converter.conversation_converter import ConversationConverter
from dao.conversation_dao import ConversationDAO
from models.conversation import Conversation
from service.persona_domain.introspection_service import IntrospectionService
from service.persona_domain.monologue_service import MonologueService
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.reasoning_conversation_service import ReasoningConversationService
from service.persona_domain.story_conversation_service import StoryConversationService


class ConversationDataService:
    def __init__(self, conversation_dao: ConversationDAO, conversation_converter: ConversationConverter,
                 persona_service: PersonaService,
                 introspection_service: IntrospectionService,
                 story_conversation_service: StoryConversationService,
                 monologue_service: MonologueService,
                 reasoning_service: ReasoningConversationService):
        self.conversation_dao = conversation_dao
        self.conversation_converter = conversation_converter
        self.persona_service = persona_service
        self.introspection_service = introspection_service
        self.story_conversation_service = story_conversation_service
        self.monologue_service = monologue_service
        self.reasoning_service = reasoning_service


    def generate(self, persona_id: int) -> List[Conversation]:

        result: List[Conversation] = []
        print(f"finding persona with id {persona_id}")
        persona = self.persona_service.find_by_id(persona_id)
        life_events = persona.life_events
        for event in life_events:
            if event.story is not None:
                story_conversation = self.story_conversation_service.find_by_story_id(event.story.id)
                if story_conversation is not None:
                    result.append(story_conversation)
        logging.info(f"returning {len(result)} conversations")
        return result