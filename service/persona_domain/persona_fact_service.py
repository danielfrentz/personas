from typing import List

from converter.persona_fact_converter import PersonaFactConverter
from dao.persona_fact_dao import PersonaFactDAO
from models.ai.input.persona_fact_input import PersonaFactInput
from models.ai.output.persona_fact_ai import PersonaFactAI
from models.persona_fact import PersonaFact
from service.ai.ai_service import AIService
from service.persona_domain.backstory_service import BackstoryService


class PersonaFactService:
    def __init__(self, ai_service: AIService,
                 backstory_service: BackstoryService,
                 persona_fact_converter: PersonaFactConverter,
                 persona_fact_dao: PersonaFactDAO):
        self.ai_service = ai_service
        self.backstory_service = backstory_service
        self.persona_fact_converter = persona_fact_converter
        self.persona_fact_dao = persona_fact_dao

    def generate(self, persona_id: int, universe_id: int) -> PersonaFact:
        """
        Generate a persona fact for a persona using the selected AI model.
        :param persona_id: The id of the persona for whom the fact is generated.
        :param universe_id: The id of the universe in which the persona is located.
        :return: The generated persona fact. This will not contain an id as it will not be saved.
        """
        user_data = PersonaFactInput(
            backstory=self.backstory_service.find_by_persona_id(persona_id=persona_id),
            existing_facts=self.find_by_persona_id(persona_id=persona_id)
        )
        generated_persona_fact = self.ai_service.call_llm(
            user_data=user_data,
            system_prompt_name="create_persona_fact",
            universe_id=universe_id,
            return_type=PersonaFactAI,
            validator=self.validate(user_data)
        )
        return self.persona_fact_converter.ai_to_model(generated_persona_fact)

    def validate(self, persona_fact_input: PersonaFactInput):
        def validation(persona_fact: PersonaFactAI):
            if persona_fact.fact_name.lower() in [fact.fact for fact in persona_fact_input.existing_facts]:
                raise ValueError(f"The fact {persona_fact.fact} has already been used, choose another one that has not been used.")
        return validation
    def find_by_persona_id(self, persona_id: int) -> List[PersonaFact]:
        """
        Find all persona facts for a persona by persona id
        :param persona_id: The id of the persona to whom the facts belong.
        :return: The facts for the persona.
        """
        persona_fact_entities = self.persona_fact_dao.find_by_persona_id(persona_id=persona_id)
        return [self.persona_fact_converter.entity_to_model(persona_fact_entity) for persona_fact_entity in persona_fact_entities]

    def save(self, persona_fact: PersonaFact, persona_id: int) -> PersonaFact:
        """
        Save a persona fact to the database under the given persona id.
        :param persona_fact: The persona fact to save.
        :param persona_id: The persona id to which the persona fact belongs.
        :return: The saved persona fact. Will contain the id of the persona fact.
        """
        persona_fact.persona_id = persona_id
        persona_fact_entity = self.persona_fact_converter.model_to_entity(persona_fact)
        persona_fact_entity = self.persona_fact_dao.save(persona_fact_entity)
        return self.persona_fact_converter.entity_to_model(persona_fact_entity)