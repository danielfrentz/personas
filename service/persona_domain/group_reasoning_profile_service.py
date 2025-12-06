from converter.group_reasoning_converter import GroupReasoningConverter
from dao.group_reasoning_style_dao import GroupReasoningStyleDAO
from models.ai.input.group_reasoning_style_input import GroupReasoningStyleInput
from models.ai.output.group_reasoning_style_ai import GroupReasoningStyleAI
from models.group_reasoning_style import GroupReasoningStyle
from service.ai.ai_service import AIService
from service.persona_domain.persona_service import PersonaService


class GroupReasoningProfileService:
    def __init__(self, ai_service: AIService,
                 persona_service: PersonaService,
                 group_reasoning_converter: GroupReasoningConverter,
                 group_reasoning_dao: GroupReasoningStyleDAO):
        self.ai_service = ai_service
        self.persona_service = persona_service
        self.group_reasoning_converter = group_reasoning_converter
        self.group_reasoning_dao = group_reasoning_dao

    def generate(self, universe_id, persona_id: int) -> GroupReasoningStyle:
        persona = self.persona_service.find_by_id(persona_id)
        group_reasoning_style_input: GroupReasoningStyleInput = GroupReasoningStyleInput(
            backstory=persona.backstory,
            speech_profile=persona.speech_profile,
        )
        generated_style = self.ai_service.call_llm("create_group_reasoning_profile", GroupReasoningStyleAI, group_reasoning_style_input, universe_id)

        return self.group_reasoning_converter.ai_to_model(generated_style, persona_id=persona_id)



    def save(self, group_reasoning_style: GroupReasoningStyle, persona_id: int):
        group_reasoning_style_entity = self.group_reasoning_converter.model_to_entity(group_reasoning_style)
        self.group_reasoning_dao.save(group_reasoning_style_entity)
        return self.group_reasoning_converter.model_to_entity(group_reasoning_style)

    def delete(self, group_reasoning_style_id: int):
        self.group_reasoning_dao.delete(group_reasoning_style_id)
