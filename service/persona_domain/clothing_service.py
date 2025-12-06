from typing import List

from converter.clothing_converter import ClothingConverter
from dao.clothing_dao import ClothingDAO
from models.ai.input.clothing_input import ClothingInput
from models.ai.output.clothing_ai import ClothingAI
from models.clothing import Clothing
from service.ai.ai_service import AIService
from service.persona_domain.backstory_service import BackstoryService
from service.persona_domain.physical_description_service import PhysicalDescriptionService
from service.persona_domain.universe_service import UniverseService


class ClothingService:
    def __init__(self, ai_service: AIService,
                 clothing_dao: ClothingDAO,
                 persona_background_service: BackstoryService,
                 clothing_converter: ClothingConverter,
                 universe_service: UniverseService,
                 physical_description_service: PhysicalDescriptionService):
        self.ai_service = ai_service
        self.clothing_dao = clothing_dao
        self.persona_background_service = persona_background_service
        self.clothing_converter = clothing_converter
        self.physical_description_service = physical_description_service
        self.universe_service = universe_service

    def generate(self, persona_id: int, universe_id: int) -> Clothing:
        backstory = self.persona_background_service.find_by_persona_id(persona_id)
        physical_description = self.physical_description_service.find_by_persona_id(persona_id)
        physical_description_id = physical_description.id
        existing_clothing = self.find_by_persona_id(persona_id=persona_id)
        clothing_input = ClothingInput(
            backstory=backstory,
            existing_clothing=existing_clothing,
            physical_description=physical_description
        )
        generated_clothing:ClothingAI = self.ai_service.call_llm("create_clothing",
                                                                 ClothingAI,
                                                                 clothing_input,
                                                                 validator=self.validate(clothing_input),
                                                                 universe_id=universe_id)
        return self.clothing_converter.ai_to_model(generated_clothing, physical_description_id=physical_description_id)

    def validate(self, clothing_input: ClothingInput):
        def validation(clothing: ClothingAI):
            if clothing.clothing_name.lower() in [clothing.clothing_name for clothing in clothing_input.existing_clothing]:
                raise ValueError(f"Clothing must be unique, but has the same name as {clothing.clothing_name}")
        return validation
    def save(self, clothing: Clothing, persona_id: int):
        clothing_entity = self.clothing_converter.model_to_entity(clothing)
        clothing_entity.physical_description_id = self.physical_description_service.find_by_persona_id(persona_id=persona_id).id
        clothing_entity = self.clothing_dao.save(clothing_entity)
        return self.clothing_converter.entity_to_model(clothing_entity)

    def find_by_persona_id(self, persona_id: int) -> List[Clothing]:
        return self.physical_description_service.find_by_persona_id(persona_id).clothing

    def delete(self, clothing_id: int):
        self.clothing_dao.delete(clothing_id)

    def find_by_id(self, clothing_id: int) -> Clothing:
        return self.clothing_converter.entity_to_model(self.clothing_dao.find_by_id(clothing_id))