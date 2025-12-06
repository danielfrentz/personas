import logging
from typing import List

from converter.accessory_converter import AccessoryConverter
from dao.accessory_dao import AccessoryDAO
from models.accessory import Accessory
from models.ai.input.accessory_input import AccessoryInput
from models.ai.output.accessory_ai import AccessoryAI
from service.ai.ai_service import AIService
from service.persona_domain.backstory_service import BackstoryService
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.physical_description_service import PhysicalDescriptionService
from service.persona_domain.universe_description_service import UniverseDescriptionService

logger = logging.getLogger(__name__)


class AccessoryService:
    def __init__(self,
                 accessory_dao: AccessoryDAO,
                 accessory_converter: AccessoryConverter,
                 ai_service: AIService,
                 backstory_service: BackstoryService,
                 physical_description_service: PhysicalDescriptionService,
                 universe_description_service: UniverseDescriptionService,
                 persona_service: PersonaService,
                 ):
        self.accessory_dao = accessory_dao
        self.accessory_converter = accessory_converter
        self.ai_service = ai_service
        self.backstory_service = backstory_service
        self.physical_description_service = physical_description_service
        self.universe_description_service = universe_description_service
        self.persona_service = persona_service

    def generate(self, persona_id: int, universe_id) -> Accessory:
        logger.info("Starting accessory generation process")
        physical_description = self.physical_description_service.find_by_persona_id(persona_id)
        physical_description_id = physical_description.id
        persona = self.persona_service.find_by_id(persona_id)

        logger.debug("Retrieving existing accessories for physical description ID %d", physical_description_id)
        existing_accessories = [accessory for accessory in self.get_by_physical_description_id(physical_description_id)]

        logger.info(f"Creating accessory input with {len(existing_accessories)} existing accessories")
        accessory_input = AccessoryInput(
            backstory=persona.backstory,
            existing_accessories=existing_accessories,
            physical_description=persona.physical_description
        )
        generated_accessory: AccessoryAI = self.ai_service.call_llm("create_accessory",
                                                                    return_type=AccessoryAI,
                                                                    user_data=accessory_input,
                                                                    universe_id=universe_id)

        logger.info("Successfully generated new accessory")
        return self.accessory_converter.ai_to_model(generated_accessory, physical_description_id)

    def validate(self, accessory_input: AccessoryInput):
        def validation(accessory: AccessoryAI):
            if accessory.accessory_name.lower() in accessory_input.existing_accessories:
                raise ValueError(f"Accessory must be unique, but has the same name as {accessory.accessory_name}")
        return validation
    def get_by_physical_description_id(self, physical_description_id: int) -> List[Accessory]:
        logger.debug("Fetching accessories for physical description ID %d", physical_description_id)
        accessory_entities = self.accessory_dao.get_by_physical_description_id(
            physical_description_id=physical_description_id)
        return [self.accessory_converter.entity_to_model(accessory) for accessory in accessory_entities]


    def save(self, accessory, persona_id: int):
        accessory_entity = self.accessory_converter.model_to_entity(accessory)
        accessory_entity.physical_description_id = self.physical_description_service.find_by_persona_id(persona_id).id
        accessory_entity = self.accessory_dao.save(accessory_entity)
        return self.accessory_converter.entity_to_model(accessory_entity)

    def get_by_persona_id(self, persona_id) -> List[Accessory]:
        return self.physical_description_service.find_by_persona_id(persona_id).accessories

    def delete(self, accessory_id: int):
        self.accessory_dao.delete(accessory_id)

    def find_by_id(self, accessory_id: int) -> Accessory:
        return self.accessory_converter.entity_to_model(self.accessory_dao.find_by_id(accessory_id))