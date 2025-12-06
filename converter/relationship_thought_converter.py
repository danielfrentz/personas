from entity.base import RelationshipThoughtEntity
from models.ai.output.relationship_thought_ai import RelationshipThoughtAI
from models.relationship_thought import RelationshipThought


class RelationshipThoughtConverter:
    def model_to_entity(self, relationship_thought: RelationshipThought) -> RelationshipThoughtEntity:
        return RelationshipThoughtEntity(
            thought=relationship_thought.thought
        )

    def entity_to_model(self, relationship_thought: RelationshipThoughtEntity) -> RelationshipThought:
        return RelationshipThought(
            thought=relationship_thought.thought,
            id=relationship_thought.id
        )

    def ai_to_model(self, relationship_thought_ai: RelationshipThoughtAI) -> RelationshipThought:
        return RelationshipThought(
            thought=relationship_thought_ai.thought
        )