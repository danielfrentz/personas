from typing import List

from converter.relationship_feeling_converter import RelationshipFeelingConverter
from converter.relationship_thought_converter import RelationshipThoughtConverter
from entity.base import PersonaRelationshipEntity, RelationshipFeelingEntity, RelationshipThoughtEntity
from models.ai.output.initial_relationship_ai import InitialRelationshipAI
from models.relationship import Relationship
from models.relationship_feeling import RelationshipFeeling
from models.relationship_thought import RelationshipThought


class RelationshipConverter:
    def __init__(self, relationship_feeling_converter: RelationshipFeelingConverter,
                 relationship_thought_converter: RelationshipThoughtConverter):
        self.relationship_feeling_converter = relationship_feeling_converter
        self.relationship_thought_converter = relationship_thought_converter

    def model_to_entity(self, model: Relationship) -> PersonaRelationshipEntity:
        converted_thoughts: List[RelationshipThoughtEntity] = [self.relationship_thought_converter.model_to_entity(thought)
                                                         for thought in model.thoughts]
        converted_feelings: List[RelationshipFeelingEntity] = [self.relationship_feeling_converter.model_to_entity(feeling)
                                                         for feeling in model.feelings]
        result = PersonaRelationshipEntity(
            id=model.id,
            source_id=model.source_id,
            target_id=model.target_id,
            relationship_type=model.relationship_type,
            overall_description=model.overall_description,
            relationship_subtype=model.relationship_subtype
        )
        result.thoughts = converted_thoughts
        result.feelings = converted_feelings
        return result


    def entity_to_model(self, persona_relationship_entity: PersonaRelationshipEntity) -> Relationship:
        converted_thoughts: List[RelationshipThought] = [self.relationship_thought_converter.entity_to_model(thought) for thought in persona_relationship_entity.thoughts]
        converted_feelings: List[RelationshipFeeling] = [self.relationship_feeling_converter.entity_to_model(feeling) for feeling in persona_relationship_entity.feelings]
        return Relationship(
            id=persona_relationship_entity.id,
            source_id=persona_relationship_entity.source_id,
            target_id=persona_relationship_entity.target_id,
            thoughts=converted_thoughts,
            feelings=converted_feelings,
            relationship_type=persona_relationship_entity.relationship_type,
            relationship_subtype=persona_relationship_entity.relationship_subtype,
            overall_description=persona_relationship_entity.overall_description
        )

    def ai_to_model(self, initial_relationship_ai: InitialRelationshipAI, persona_id: int, other_persona_id: int) -> Relationship:
        return Relationship(
            source_id = persona_id,
            target_id = other_persona_id,
            relationship_type = initial_relationship_ai.relationship_type,
            relationship_subtype = initial_relationship_ai.relationship_subtype,
            overall_description=initial_relationship_ai.relationship_description,
        )