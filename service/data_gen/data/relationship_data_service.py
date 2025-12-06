import logging
from typing import List

from models.conversation import Conversation
from models.conversation_turn import ConversationTurn
from service.persona_domain.persona_service import PersonaService


class RelationshipDataService:
    relationship_type_conversation_turn = "I have a {relationship_type} relationship with you."
    def __init__(self, persona_service: PersonaService):
        self.persona_service = persona_service

    def generate(self, persona_id) -> List[Conversation]:
        result: List[Conversation] = []
        persona = self.persona_service.find_by_id(persona_id)
        for relationship in persona.relationships:
            target_persona = self.persona_service.find_by_id(relationship.target_id)
            target_persona_to_persona_relationship = [target_relationship for target_relationship in target_persona.relationships if relationship.target_id == persona_id]
            if len(target_persona_to_persona_relationship) > 0:
                target_persona_to_persona_relationship = target_persona_to_persona_relationship[0]
                conversation_relationship_type_query = ConversationTurn(
                    text=f"I feel I have a {target_persona_to_persona_relationship.relationship_type} relationship with you which i'd classify as {target_persona_to_persona_relationship.relationship_subtype}, what kind of relationship do you feel you have with me?",
                    directed_at=[persona.backstory.name],
                    action=f"Exchanging relationship types with {persona.backstory.name}",
                    tone="curious",
                    speaker=target_persona.backstory.name,
                    feeling="curious"
                )
                conversation_relationship_type = ConversationTurn(
                    text=f"In my case I think I have a {relationship.relationship_type} relationship with you which i'd classify as {relationship.relationship_subtype}.",
                    directed_at=[target_persona.backstory.name],
                    speaker=persona.backstory.name,
                    tone="calm",
                    feeling="neutral"
                )
                relationship_type_conversation = Conversation(
                    conversation_turns=[conversation_relationship_type_query, conversation_relationship_type]
                )
                result.append(relationship_type_conversation)
            for thought in relationship.thoughts:
                conversation_relationship_thoughts = ConversationTurn(
                    text=thought.thought,
                    directed_at=[persona.backstory.name],
                    action=f"Considering what I think about {target_persona.backstory.name}",
                    speaker=persona.backstory.name,
                    tone="calm",
                    feeling="neutral"
                )
                result.append(Conversation(conversation_turns=[conversation_relationship_thoughts]))
        logging.info(f"returning {len(result)} relationships")
        return result
