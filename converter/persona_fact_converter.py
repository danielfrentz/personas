from entity.base import PersonaFactEntity
from models.ai.output.persona_fact_ai import PersonaFactAI
from models.persona_fact import PersonaFact


class PersonaFactConverter:
    def model_to_entity(self, persona_fact: PersonaFact) -> PersonaFactEntity:
        return PersonaFactEntity(
            fact=persona_fact.fact.lower(),
            fact_explanation=persona_fact.fact_explanation,
            id=persona_fact.id,
            persona_id=persona_fact.persona_id
        )

    def entity_to_model(self, persona_fact_entity: PersonaFactEntity) -> PersonaFact:
        return PersonaFact(
            fact=persona_fact_entity.fact.lower(),
            fact_explanation=persona_fact_entity.fact_explanation,
            id=persona_fact_entity.id,
            persona_id=persona_fact_entity.persona_id
        )

    def ai_to_model(self, persona_fact_ai: PersonaFactAI) -> PersonaFact:
        return PersonaFact(
            fact=persona_fact_ai.fact_name.lower(),
            fact_explanation=persona_fact_ai.fact_explanation
        )
