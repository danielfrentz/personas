from converter.physical_description_converter import PhysicalDescriptionConverter
from dao.physical_description_dao import PhysicalDescriptionDAO
from models.ai.output.physical_description_ai import PhysicalDescriptionAI
from models.physical_description import PhysicalDescription, PhysicalDescriptionInput
from service.ai.ai_service import AIService
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.universe_description_service import UniverseDescriptionService


class PhysicalDescriptionService:
    def __init__(self,
                 ai_service: AIService,
                 persona_service: PersonaService,
                 physical_description_dao: PhysicalDescriptionDAO,
                 physical_description_converter: PhysicalDescriptionConverter,
                 universe_description_service: UniverseDescriptionService):
        self.persona_service = persona_service
        self.ai_service = ai_service
        self.physical_description_dao = physical_description_dao
        self.physical_description_converter = physical_description_converter
        self.universe_description_service = universe_description_service

    def generate(self, persona_id: int, universe_id:int) -> PhysicalDescription:
        persona = self.persona_service.find_by_id(persona_id)
        universe_description = self.universe_description_service.find_by_id(persona.universe_id)
        physical_description_data = PhysicalDescriptionInput(
            backstory=persona.backstory,
            universe=universe_description
        )
        generated_physical_description: PhysicalDescriptionAI = self.ai_service.call_llm("create_physical_description", user_data=physical_description_data, universe_id=universe_id, return_type=PhysicalDescriptionAI)
        return self.physical_description_converter.ai_to_model(generated_physical_description)

    def save(self, physical_description: PhysicalDescription, persona_id: int):
        physical_description_entity = self.physical_description_converter.model_to_entity(physical_description)
        physical_description_entity.persona_id = persona_id
        physical_description_entity = self.physical_description_dao.save(physical_description_entity)
        return self.physical_description_converter.entity_to_model(physical_description_entity)

    def find_by_id(self, physical_description_id):
        return self.physical_description_dao.find_by_persona_id(physical_description_id)

    def find_by_persona_id(self, persona_id) -> PhysicalDescription:
        physical_description_entity = self.physical_description_dao.find_by_persona_id(persona_id)
        return self.physical_description_converter.entity_to_model(physical_description_entity)

    def delete(self, physical_description_id):
        self.physical_description_dao.delete(physical_description_id)

