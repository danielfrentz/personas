from converter.conversation_converter import ConversationConverter
from converter.conversation_turn_converter import ConversationTurnConverter
from entity.base import IntrospectionEntity
from models.ai.output.introspection_ai import IntrospectionAI
from models.introspection import Introspection
from models.persona import Persona


class IntrospectionConverter:
    def __init__(self, conversation_converter: ConversationConverter,
                 conversation_turn_converter: ConversationTurnConverter,):
        self.conversation_converter = conversation_converter
        self.conversation_turn_converter = conversation_turn_converter

    def model_to_entity(self, introspection: Introspection) -> IntrospectionEntity:
        return IntrospectionEntity(
            story_id=introspection.story_id,
            id=introspection.id,
            personality_aspect_role=introspection.personality_aspect_role,
            introspection_topic=introspection.introspection_topic,
            aspect_id=introspection.aspect_id,
        )

    def entity_to_model(self, introspection_entity: IntrospectionEntity) -> Introspection:
        return Introspection(
            id=introspection_entity.id,
            introspection_topic=introspection_entity.introspection_topic,
            story_id=introspection_entity.story_id,
            aspect_id=introspection_entity.aspect_id,
            personality_aspect_role=introspection_entity.personality_aspect_role
        )

    def ai_to_model(self, generated_dialogue: IntrospectionAI, persona: Persona, story_id: int) -> Introspection:
        result = Introspection(
            monologue=self.conversation_converter.ai_to_model(generated_dialogue.internal_monologue),
            story_id=story_id,
            introspection_topic=generated_dialogue.introspection_topic,
            personality_aspect_role=generated_dialogue.personality_aspect_role
        )

        return result