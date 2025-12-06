from typing import List

from converter.conversation_turn_converter import ConversationTurnConverter
from entity.base import ConversationEntity
from models.ai.output.conversation_ai import ConversationAI
from models.conversation import Conversation
from models.conversation_turn import ConversationTurn


class ConversationConverter:

    def __init__(self, conversation_turn_converter: ConversationTurnConverter):
        self.conversation_turn_converter = conversation_turn_converter

    def model_to_entity(self, conversation: Conversation) -> ConversationEntity:
        conversation_turns = [self.conversation_turn_converter.model_to_entity(conversation_turn) for conversation_turn in conversation.conversation_turns]
        for idx, conversation_turn in enumerate(conversation_turns):
            conversation_turn.placement = idx
        result = ConversationEntity(
            source_id=conversation.source_id,
            source=conversation.source_name,
        )
        result.conversation_turns = conversation_turns
        return result

    def entity_to_model(self, conversation_entity: ConversationEntity) -> Conversation | None:
        if conversation_entity is None:
            return None
        conversation_turns: List[ConversationTurn] = \
            [self.conversation_turn_converter.entity_to_model(conversation_turn_entity) for conversation_turn_entity in conversation_entity.conversation_turns]
        return Conversation(
            id=conversation_entity.id,
            source_id=conversation_entity.source_id,
            source_name=conversation_entity.source,
            conversation_turns=conversation_turns,
        )

    def ai_to_model(self, conversation_ai: ConversationAI) -> Conversation:
        conversation_turns = [self.conversation_turn_converter.ai_to_model(conversation_turn) for conversation_turn in conversation_ai.conversation_turns]
        return Conversation(
            conversation_turns=conversation_turns
        )

