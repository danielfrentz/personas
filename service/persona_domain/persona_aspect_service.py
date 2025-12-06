from converter.persona_aspect_converter import PersonaAspectConverter
from dao.persona_aspect_dao import PersonaAspectDao
from models.ai.input.persona_aspect_input import PersonaAspectInput
from models.ai.output.persona_aspect_ai import PersonaAspectAI
from models.http.request.generate.persona_aspect_request import PersonaAspectRequest
from models.persona_aspect import PersonaAspect
from service.ai.ai_service import AIService
from service.persona_domain.backstory_service import BackstoryService
from service.persona_domain.persona_service import PersonaService


class PersonaAspectService:
    def __init__(self,
                 ai_service: AIService,
                 backstory_service: BackstoryService,
                 persona_aspect_converter: PersonaAspectConverter,
                 persona_aspect_dao: PersonaAspectDao,
                 persona_service: PersonaService,):
        self.ai_service = ai_service
        self.backstory_service = backstory_service
        self.persona_aspect_converter = persona_aspect_converter
        self.persona_aspect_dao = persona_aspect_dao
        self.persona_service = persona_service

    def generate(self, persona_id: int, universe_id: int, persona_aspect_request: PersonaAspectRequest) -> PersonaAspect:
        backstory = self.backstory_service.find_by_persona_id(persona_id=persona_id)
        ai_input = PersonaAspectInput(
            aspect_name=persona_aspect_request.aspect_name,
            backstory=backstory
        )
        generated_aspect = self.ai_service.call_llm(user_data=ai_input,
                                                    system_prompt_name="create_persona_aspect",
                                                    return_type=PersonaAspectAI,
                                                    universe_id=universe_id,)
        return self.persona_aspect_converter.ai_to_model(generated_aspect, backstory_id=backstory.id, aspect_name=persona_aspect_request.aspect_name)

    def save(self, persona_id: int, persona_aspect: PersonaAspect):
        backstory_id = self.persona_service.find_by_id(persona_id=persona_id).backstory.id
        persona_aspect.backstory_id = backstory_id
        persona_aspect_entity = self.persona_aspect_converter.model_to_entity(persona_aspect)
        persona_aspect_entity = self.persona_aspect_dao.save(persona_aspect_entity)
        return self.persona_aspect_converter.entity_to_model(persona_aspect_entity)

    def find_by_persona_and_name(self, persona_id: int, aspect_name: str):
        aspect_entity = self.persona_aspect_dao.find_by_persona_and_name(persona_id=persona_id, aspect_name=aspect_name)
        return self.persona_aspect_converter.entity_to_model(aspect_entity)

    def find_by_persona(self, persona_id):
        backstory_id = self.backstory_service.find_by_persona_id(persona_id=persona_id).id
        persona_aspect_entities = self.persona_aspect_dao.find_by_backstory_id(backstory_id=backstory_id)
        return [self.persona_aspect_converter.entity_to_model(persona_aspect_entity) for persona_aspect_entity in persona_aspect_entities]

    def find_by_id(self, aspect_id):
        aspect_entity = self.persona_aspect_dao.find_by_id(aspect_id)
        return self.persona_aspect_converter.entity_to_model(aspect_entity)