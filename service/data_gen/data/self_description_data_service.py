from typing import List

from models.conversation import Conversation
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.self_description_conversation_service import SelfDescriptionConversationService


class SelfDescriptionDataService:
    def __init__(self, self_description_conversation_service: SelfDescriptionConversationService,
                 persona_service: PersonaService):
        self.self_description_conversation_service = self_description_conversation_service
        self.persona_service = persona_service

    def generate(self, persona_id) -> list[Conversation]:
        persona = self.persona_service.find_by_id(persona_id)
        result: List[Conversation] = []
        for conversation in self.self_description_conversation_service.find_by_persona_id(persona_id):
            c = conversation.conversation
            for turn in c.conversation_turns:
                if turn.speaker != persona.backstory.name:
                    turn.speaker = "User"
                if turn.directed_at != [persona.backstory.name]:
                    turn.directed_at = ["User"]

            c.conversation_turns[0].turn_intent = "self description"
            result.append(c)
        return result