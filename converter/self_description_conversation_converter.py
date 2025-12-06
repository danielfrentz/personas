from converter.conversation_converter import ConversationConverter
from entity.base import SelfDescriptionConversationEntity
from models.ai.output.self_description_conversation import SelfDescriptionConversation
from models.ai.output.self_description_conversation_ai import SelfDescriptionConversationAI


class SelfDescriptionConversationConverter:
    def __init__(self, conversation_converter: ConversationConverter):
        self.conversation_converter = conversation_converter

    def model_to_entity(self, self_description_conversation: SelfDescriptionConversation) -> SelfDescriptionConversationEntity:
        return SelfDescriptionConversationEntity(
            id=self_description_conversation.id,
            persona_id=self_description_conversation.persona_id,
            topic=self_description_conversation.topic,
            prompter_id=self_description_conversation.prompter_id,

        )

    def entity_to_model(self, self_description_conversation_entity: SelfDescriptionConversationEntity) -> SelfDescriptionConversation:
        return SelfDescriptionConversation(
            conversation=None,
             persona_id=self_description_conversation_entity.persona_id,
            id=self_description_conversation_entity.id,
            topic=self_description_conversation_entity.topic,
            prompter_id=self_description_conversation_entity.prompter_id
        )

    def ai_to_model(self, generated_conversation: SelfDescriptionConversationAI, persona_id: int, prompter_id: int, topic: str) -> SelfDescriptionConversation:
        return SelfDescriptionConversation(
            conversation=self.conversation_converter.ai_to_model(generated_conversation.conversation),
            persona_id=persona_id,
            topic=topic,
            prompter_id=prompter_id,
        )
