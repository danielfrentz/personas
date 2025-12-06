import logging
from typing import List

from converter.persona_converter import PersonaConverter
from dao.persona_dao import PersonaDAO
from models.persona import Persona
logger = logging.getLogger("ai_service")

class PersonaService:
    def __init__(self, persona_dao: PersonaDAO, persona_converter: PersonaConverter):
        self.person_dao = persona_dao
        self.persona_converter = persona_converter

    def save(self, persona: Persona):
        persona_entity = self.persona_converter.model_to_entity(persona)
        persona_entity = self.person_dao.save(persona_entity)
        return self.persona_converter.entity_to_model(persona_entity)

    def find_by_name(self, persona_name: str) -> Persona:
        persona_entity = self.person_dao.get_persona_by_name(persona_name)
        return self.persona_converter.entity_to_model(persona_entity)

    def find_by_id(self, persona_id: int) -> Persona:
        persona_entity = self.person_dao.find_by_id(persona_id)
        return self.persona_converter.entity_to_model(persona_entity)

    def find_by_universe(self, universe_id: int) -> List[Persona]:
        existing_characters_entities = self.person_dao.get_existing_persona(universe_id)
        return [self.persona_converter.entity_to_model(persona_entity=persona_entity) for persona_entity in existing_characters_entities]

    def delete(self, persona_id: int):
        self.person_dao.delete(persona_id)
