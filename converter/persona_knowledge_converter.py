from entity.base import PersonaKnowledgeEntity
from models.ai.output.persona_knowledge_ai import PersonaKnowledgeAI
from models.persona_knowledge import PersonaKnowledge


class PersonaKnowledgeConverter:
    def model_to_entity(self, persona_knowledge: PersonaKnowledge) -> PersonaKnowledgeEntity:
        return PersonaKnowledgeEntity(
            id=persona_knowledge.id,
            knowledge_name=persona_knowledge.knowledge_name,
            knowledge_description=persona_knowledge.knowledge_description,
            persona_id=persona_knowledge.persona_id
        )

    def entity_to_model(self, persona_knowledge_entity: PersonaKnowledgeEntity) -> PersonaKnowledge:
        return PersonaKnowledge(
            id=persona_knowledge_entity.id,
            knowledge_name=persona_knowledge_entity.knowledge_name,
            knowledge_description=persona_knowledge_entity.knowledge_description,
            persona_id=persona_knowledge_entity.persona_id
        )

    def ai_to_model(self, knowledge_ai: PersonaKnowledgeAI, persona_id: int) -> PersonaKnowledge:
        return PersonaKnowledge(
            knowledge_name=knowledge_ai.knowledge_name,
            knowledge_description=knowledge_ai.knowledge_description,
            persona_id=persona_id
        )