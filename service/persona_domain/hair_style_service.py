from converter.hair_style_converter import HairStyleConverter
from dao.hairstyle_dao import HairStyleDAO
from entity.base import PersonaEntity
from models.ai.output.hair_style_ai import HairStyleAI
from models.hair_style import HairStyle
from service.ai.ai_service import AIService
from service.persona_domain.backstory_service import BackstoryService


class HairStyleService:

    def __init__(self, ai_service: AIService,
                 backstory_service: BackstoryService,
                 hairstyle_converter: HairStyleConverter,
                 hair_style_dao: HairStyleDAO):
        self.backstory_service = backstory_service
        self.ai_service = ai_service
        self.hairstyle_converter = hairstyle_converter
        self.hair_style_dao = hair_style_dao

    def generate(self, persona_id: int, universe_id: int) -> PersonaEntity:
        backstory = self.backstory_service.find_by_persona_id(persona_id)
        generated_hairstyle = self.ai_service.call_llm(system_prompt_name="create_hair_style",
                                                       return_type=HairStyleAI,
                                                       user_data=backstory,
                                                       universe_id=universe_id)
        return self.hairstyle_converter.ai_to_model(generated_hairstyle)

    def save(self, physical_description_id: int, hairstyle: HairStyle):
        hairstyle_entity = self.hairstyle_converter.model_to_entity(hairstyle)
        hairstyle_entity.physical_description_id = physical_description_id
        hairstyle_entity = self.hair_style_dao.save(hairstyle_entity)
        return self.hairstyle_converter.entity_to_model(hairstyle_entity)

    def delete(self, hairstyle_id: int):
        self.hair_style_dao.delete(hairstyle_id)
