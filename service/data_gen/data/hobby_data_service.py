from typing import List

from models.conversation import Conversation
from models.conversation_turn import ConversationTurn
from models.hobby import Hobby
from service.persona_domain.hobby_service import HobbyService
from service.persona_domain.persona_service import PersonaService


class HobbyDataService:
    def __init__(self, hobby_service: HobbyService, persona_service: PersonaService):
        self.hobby_service = hobby_service
        self.persona_service = persona_service

    def generate(self, persona_id: int) -> List[Conversation]:
        persona = self.persona_service.find_by_id(persona_id)
        hobbies: List[Hobby] = self.hobby_service.find_by_persona_id(persona_id)
        result: List[Conversation] = []
        for hobby in hobbies:
            conversation_turn = ConversationTurn(
                speaker=persona.backstory.name,
                action="Explaining the hobby",
                text=f"Something I really love is {hobby.hobby_name}.",
                tone="Pensive",
                directed_at=[f"{persona.backstory.name}'s mind"],
                feeling="happy"
            )
            conversation = Conversation(
                conversation_turns=[conversation_turn]
            )
            result.append(conversation)
        return result
