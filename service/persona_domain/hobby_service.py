from converter.hobby_converter import HobbyConverter
from dao.hobby_dao import HobbyDAO
from models.ai.input.hobby_input import HobbyInput
from models.ai.output.hobby_ai import HobbyAI
from models.hobby import Hobby
from service.ai.ai_service import AIService
from service.persona_domain.backstory_service import BackstoryService


class HobbyService:
    def __init__(self, ai_service: AIService,
                 hobby_converter: HobbyConverter,
                 backstory_service: BackstoryService,
                 hobby_dao: HobbyDAO):
        self.ai_service = ai_service
        self.hobby_converter = hobby_converter
        self.backstory_service = backstory_service
        self.hobby_dao = hobby_dao

    def generate(self, persona_id: int, universe_id: int) -> Hobby:
        backstory = self.backstory_service.find_by_persona_id(persona_id=persona_id)
        user_data = HobbyInput(
            backstory=backstory
        )
        generated_hobby = self.ai_service.call_llm(system_prompt_name="create_hobby",
                                                   return_type=HobbyAI,
                                                   user_data=user_data,
                                                   universe_id=universe_id,
                                                   validator=self.create_validation(user_data))
        return self.hobby_converter.ai_to_model(generated_hobby)

    def create_validation(self, hobby_input: HobbyInput):
        def validation(hobby_ai: HobbyAI):
            if hobby_ai.name in hobby_input.backstory.hobbies:
                raise ValueError(f"Hobby must be unique, but has the same name as {hobby_ai.name}")
        return validation

    def save(self, persona_id: int, hobby: Hobby) -> Hobby:
        hobby_entity = self.hobby_converter.model_to_entity(hobby)
        hobby_entity.backstory_id = self.backstory_service.find_by_persona_id(persona_id).id
        hobby_entity = self.hobby_dao.save(hobby_entity)
        return self.hobby_converter.entity_to_model(hobby_entity)

    def delete(self, hobby_id: int):
        self.hobby_dao.delete(hobby_id)

    def find_by_persona_id(self, persona_id):
        backstory_id: int = self.backstory_service.find_by_persona_id(persona_id=persona_id).id
        hobby_entities = self.hobby_dao.find_by_backstory_id(backstory_id=backstory_id)
        return [self.hobby_converter.entity_to_model(hobby) for hobby in hobby_entities]
