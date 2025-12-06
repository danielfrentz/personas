from converter.backstory_converter import BackstoryConverter
from dao.backstory_dao import BackstoryDAO
from models.ai.input.backstory_input import BackstoryInput
from models.ai.output.backstory_ai import BackstoryAI
from models.backstory import Backstory
from models.http.request.generate.backstory_generate_request import BackstoryGenerateRequest
from service.ai.ai_service import AIService
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.universe_description_service import UniverseDescriptionService


class BackstoryService:
    """Service for managing and generating backstories for personas within a universe.

    This service handles the creation, storage, and retrieval of backstories associated with
    personas in a given universe. It leverages AI services to generate detailed backstories
    and interacts with data access objects (DAO) for persistence.

    Attributes:
        ai_service: Service used to generate content via AI.
        backstory_dao: Data access object for managing backstory entities.
        backstory_converter: Converts between model and entity representations.
        universe_description_service: Provides universe descriptions for backstory generation.
        persona_service: Manages access to persona data.
    """
    def __init__(self, ai_service: AIService,
                 backstory_dao: BackstoryDAO,
                 backstory_converter: BackstoryConverter,
                 universe_description_service: UniverseDescriptionService,
                 persona_service: PersonaService,
                 ):
        self.ai_service = ai_service
        self.backstory_dao = backstory_dao
        self.backstory_converter = backstory_converter
        self.universe_description_service = universe_description_service
        self.persona_service = persona_service

    def generate(self, request: BackstoryGenerateRequest, universe_id: int) -> Backstory:
        universe_description = self.universe_description_service.find_by_universe_id(universe_id)
        backstory_data = BackstoryInput(name=request.name,
                                        initial_character_description=request.description,
                                        historical=request.historical,
                                        universe=universe_description)
        generated_backstory = self.ai_service.call_llm(system_prompt_name="create_back_story",
                                                   return_type=BackstoryAI,
                                                   user_data=backstory_data,
                                                   universe_id=universe_id)
        print(f"got request as {request.historical}")
        result = self.backstory_converter.ai_to_model(backstory_ai=generated_backstory, name=request.name, historical=request.historical)
        result.historical = request.historical
        result.name = request.name
        return result

    def save(self, backstory: Backstory, persona_id: int) -> Backstory:
        backstory_entity = self.backstory_converter.model_to_entity(backstory, persona_id)
        backstory_entity = self.backstory_dao.save(backstory_entity)
        return self.backstory_converter.entity_to_model(backstory_entity)

    def find_by_persona_id(self, persona_id) -> Backstory:
        backstory_entity = self.backstory_dao.find_by_persona_id(persona_id)
        return self.backstory_converter.entity_to_model(backstory_entity)

    def find_by_id(self, backstory_id) -> Backstory:
        backstory_entity = self.backstory_dao.find_by_id(backstory_id)
        return self.backstory_converter.entity_to_model(backstory_entity)

    def find_by_name(self, name) -> Backstory:
        backstory_entity = self.backstory_dao.find_by_persona_name(name)
        return self.backstory_converter.entity_to_model(backstory_entity)

    def delete(self, backstory_id: int):
        self.backstory_dao.delete(backstory_id)

    def find_all(self):
        backstory_entities = self.backstory_dao.find_all()
        return [self.backstory_converter.entity_to_model(backstory_entity=backstory_entity) for backstory_entity in backstory_entities]



