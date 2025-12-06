from converter.conversation_converter import ConversationConverter
from entity.base import ReasoningConversationEntity
from models.conversation import Conversation
from models.reasoning_conversation import ReasoningConversation


class ReasoningConversationConverter:

    def __init__(self, conversation_converter: ConversationConverter,):
        self.conversation_converter = conversation_converter

    def model_to_entity(self, reasoning_conversation: ReasoningConversation) -> ReasoningConversationEntity:
        conversation_entity = self.conversation_converter.model_to_entity(reasoning_conversation.conversation)
        reasoning_entity = ReasoningConversationEntity(
            problem_statement=reasoning_conversation.problem_statement,
            persona_id=reasoning_conversation.persona_id,
            theme=reasoning_conversation.theme,
        )
        reasoning_entity.conversation = conversation_entity
        reasoning_entity.conversation.source = ReasoningConversation.__name__
        return reasoning_entity

    def entity_to_model_without_conversation(self, reasoning_entity: ReasoningConversationEntity) -> ReasoningConversation:
        return ReasoningConversation(
            id=reasoning_entity.id,
            problem_statement=reasoning_entity.problem_statement,
            conversation=Conversation(conversation_turns=[]),
            persona_id=reasoning_entity.persona_id,
            theme=reasoning_entity.theme
        )
    def entity_to_model(self, reasoning_entity: ReasoningConversationEntity) -> ReasoningConversation:
        conversation_model = self.conversation_converter.entity_to_model(reasoning_entity.conversation)
        return ReasoningConversation(
            id=reasoning_entity.id,
            problem_statement=reasoning_entity.problem_statement,
            conversation=conversation_model,
            persona_id=reasoning_entity.persona_id,
            theme=reasoning_entity.theme
        )

    def ai_to_model(self, dialogue: Conversation, problem_statement: str, persona_id: int, theme: str, extends: int = None) -> ReasoningConversation:
        return ReasoningConversation(
            conversation=Conversation(conversation_turns=dialogue.conversation_turns),
            problem_statement=problem_statement,
            persona_id=persona_id,
            theme=theme
        )