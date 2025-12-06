from entity.base import ConversationTurnEntity, ConversationTurnDirectedAtEntity
from models.ai.output.conversation_turn_ai import ConversationTurnAI
from models.conversation import ConversationTurn


class ConversationTurnConverter:
    def model_to_entity(self, conversation: ConversationTurn) -> ConversationTurnEntity:
        result = ConversationTurnEntity(
            action=conversation.action,
            text=conversation.text,
            speaker=conversation.speaker,
            tone=conversation.tone,
            placement=conversation.placement,
            feeling=conversation.feeling,
            private_thought=conversation.private_thought,
            turn_intent=conversation.turn_intent,
        )
        result.directed_at = [ConversationTurnDirectedAtEntity(persona_name=directed_at) for directed_at in conversation.directed_at]
        return result


    def entity_to_model(self, conversation_turn_entity: ConversationTurnEntity) -> ConversationTurn:
        directed_at = [directed_at.persona_name for directed_at in conversation_turn_entity.directed_at]
        feeling = conversation_turn_entity.feeling
        if feeling is None:
            feeling = "neutral"
        tone = conversation_turn_entity.tone
        if tone is None:
            tone = "neutral"
        return ConversationTurn(
            id=conversation_turn_entity.id,
            tone=conversation_turn_entity.tone,
            speaker=conversation_turn_entity.speaker,
            text=conversation_turn_entity.text,
            action=conversation_turn_entity.action,
            placement=conversation_turn_entity.placement,
            directed_at=directed_at,
            feeling=feeling,
            private_thought=conversation_turn_entity.private_thought,
            turn_intent=conversation_turn_entity.turn_intent,
        )

    def ai_to_model(self, conversation_turn: ConversationTurnAI) -> ConversationTurn:
        return ConversationTurn(
            action=conversation_turn.action,
            text=conversation_turn.text,
            speaker=conversation_turn.speaker,
            directed_at=conversation_turn.directed_at,
            tone=conversation_turn.tone,
            feeling=conversation_turn.feeling,
            private_thought=conversation_turn.private_thought,
            turn_intent=conversation_turn.turn_purpose,
        )

