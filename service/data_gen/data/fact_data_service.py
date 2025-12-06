from typing import List

from models.conversation import Conversation
from models.conversation_turn import ConversationTurn
from service.persona_domain.persona_fact_service import PersonaFactService
from service.persona_domain.persona_service import PersonaService


class FactDataService:
    """
    Service class used to generate the training data for persona facts.
    """
    def __init__(self, fact_service: PersonaFactService,
                 persona_service: PersonaService):
        self.fact_service = fact_service
        self.persona_service = persona_service

    def generate(self, persona_id: int) -> List[Conversation]:
        persona = self.persona_service.find_by_id(persona_id)
        facts = self.fact_service.find_by_persona_id(persona_id=persona_id)
        result: List[Conversation] = []
        for fact in facts:
            turn = ConversationTurn(
                speaker=persona.backstory.name,
                directed_at=["everyone"],
                text=fact.fact_explanation,
                tone="Pensive",
                action=f"Explaining why the fact {fact.fact} applies to myself",
                feeling="confident"
            )
            result.append(Conversation(conversation_turns=[turn]))
        return result