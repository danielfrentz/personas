from converter.conversation_converter import ConversationConverter
from entity.base import MonologueEntity
from models.ai.input.monologue import MonologueInput
from models.ai.output.monologue_ai import MonologueAI
from models.monologue import Monologue


class MonologueConverter:
    def __init__(self, conversation_converter: ConversationConverter):
        self.conversation_converter = conversation_converter

    def model_to_entity(self, monologue: Monologue) -> MonologueEntity:
        result = MonologueEntity(
            prompter_id=monologue.prompter_id,
            theme=monologue.theme,
            speaker_id=monologue.speaker_id,
            prompt=monologue.prompt,
            deliverable=monologue.deliverable,
            problem_type=monologue.problem_type,
            trigger_word=monologue.trigger_word
        )
        result.conversation = self.conversation_converter.model_to_entity(monologue.conversation)
        result.conversation.source = Monologue.__name__
        return result

    def entity_to_model(self, monologue_entity: MonologueEntity) -> Monologue:
        converted_conversation = self.conversation_converter.entity_to_model(monologue_entity.conversation)
        return Monologue(
            id=monologue_entity.id,
            theme=monologue_entity.theme,
            speaker_id=monologue_entity.speaker_id,
            prompter_id=monologue_entity.prompter_id,
            conversation=converted_conversation,
            prompt=monologue_entity.prompt,
            deliverable=monologue_entity.deliverable,
            problem_type=monologue_entity.problem_type,
            trigger_word=monologue_entity.trigger_word
        )

    def ai_to_model(self, generated_monologue: MonologueAI, monologue_input: MonologueInput, theme: str) -> Monologue:
        converted_conversation = self.conversation_converter.ai_to_model(generated_monologue.conversation)
        result = Monologue(
            theme=theme,
            conversation=converted_conversation,
            prompt=monologue_input.prompt,
            deliverable=generated_monologue.deliverable,
            problem_type=monologue_input.problem_type
        )

        return result