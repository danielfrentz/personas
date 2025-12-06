from entity.base import RelationshipFeelingEntity
from models.ai.output.relationship_feelng_ai import RelationshipFeelingAI
from models.relationship_feeling import RelationshipFeeling


class RelationshipFeelingConverter:
    def model_to_entity(self, relationship_feeling_model: RelationshipFeeling) -> RelationshipFeelingEntity:
        return RelationshipFeelingEntity(
            feeling_name=relationship_feeling_model.feeling_name,
            persona_relationship_id=relationship_feeling_model.persona_relationship_id,
            id=relationship_feeling_model.id,
            reason=relationship_feeling_model.reason
        )

    def entity_to_model(self, relationship_feeling_entity: RelationshipFeelingEntity) -> RelationshipFeeling:
        return RelationshipFeeling(
            id=relationship_feeling_entity.id,
            persona_relationship_id=relationship_feeling_entity.persona_relationship_id,
            feeling_name=relationship_feeling_entity.feeling_name,
            reason=relationship_feeling_entity.reason
        )

    def ai_to_model(self, relationship_feeling_ai: RelationshipFeelingAI, source_persona_id:int ) -> RelationshipFeeling:
        return RelationshipFeeling(
            feeling_name=relationship_feeling_ai.feeling_name,
            reason=relationship_feeling_ai.reason,
            persona_relationship_id=source_persona_id

        )