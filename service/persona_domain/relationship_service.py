from typing import List

from converter.relationship_converter import RelationshipConverter
from dao.relationship_dao import RelationshipDAO
from models.ai.output.initial_relationship_ai import InitialRelationshipAI
from models.http.relationship_request import RelationshipRequest
from models.initial_relationship import InitialRelationshipInput
from models.relationship import Relationship
from service.ai.ai_service import AIService
from service.persona_domain.backstory_service import BackstoryService
from service.persona_domain.persona_service import PersonaService


class RelationshipService:
    def __init__(self, ai_service: AIService, backstory_service: BackstoryService,
                 persona_service: PersonaService, relationship_converter: RelationshipConverter,
                 relationship_dao: RelationshipDAO):
        self.ai_service = ai_service
        self.backstory_service = backstory_service
        self.persona_service = persona_service
        self.relationship_converter = relationship_converter
        self.relationship_dao = relationship_dao

    def generate(self, universe_id: int, relationship_request: RelationshipRequest) -> Relationship:
        source_persona_backstory = self.backstory_service.find_by_persona_id(relationship_request.source_persona_id)
        target_persona_backstory = self.backstory_service.find_by_persona_id(relationship_request.target_persona_id)
        relationship_input = InitialRelationshipInput(source_persona=source_persona_backstory,
                                                              target_persona=target_persona_backstory)
        generated_relationship: InitialRelationshipAI = self.ai_service.call_llm(
            system_prompt_name="create_initial_relationships",
            return_type=InitialRelationshipAI,
            user_data=relationship_input,
            universe_id=universe_id)

        return self.relationship_converter.ai_to_model(generated_relationship, other_persona_id=relationship_request.target_persona_id,
                                                    persona_id=relationship_request.source_persona_id)

    def save(self, relationship: Relationship):
        relationship_entity = self.relationship_converter.model_to_entity(relationship)
        existing = self.relationship_dao.find_by_id_source_target(relationship.source_id, relationship.target_id)
        if existing:
            self.relationship_dao.update(relationship_entity, existing.id)
        else:
            relationship_entity = self.relationship_dao.save(relationship_entity)
        return self.relationship_converter.entity_to_model(relationship_entity)

    def get_by_persona_id(self, persona_id: int) -> List[Relationship]:
        relationship_entities = self.relationship_dao.find_by_persona_id(persona_id)
        return [self.relationship_converter.entity_to_model(relationship) for relationship in relationship_entities]

    def delete(self, relationship_id: int):
        self.relationship_dao.delete(relationship_id)
