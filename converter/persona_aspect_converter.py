from entity.base import PersonaAspectEntity
from models.ai.output.persona_aspect_ai import PersonaAspectAI
from models.persona_aspect import PersonaAspect


class PersonaAspectConverter:
    def model_to_entity(self, persona_aspect: PersonaAspect) -> PersonaAspectEntity:
        return PersonaAspectEntity(
            aspect_name=persona_aspect.aspect_name,
            aspect_description=persona_aspect.aspect_description,
            backstory_id=persona_aspect.backstory_id,
            id=persona_aspect.id,
            strength_of_aspect_in_personality=persona_aspect.strength_of_aspect_in_personality
        )

    def entity_to_model(self, persona_aspect: PersonaAspectEntity) -> PersonaAspect:
        return PersonaAspect(
            aspect_name=persona_aspect.aspect_name,
            aspect_description=persona_aspect.aspect_description,
            id=persona_aspect.id,
            strength_of_aspect_in_personality=persona_aspect.strength_of_aspect_in_personality,
            backstory_id=persona_aspect.backstory_id
        )

    def ai_to_model(self, persona_aspect: PersonaAspectAI, backstory_id: int, aspect_name: str) -> PersonaAspect:
        return PersonaAspect(
            aspect_name=aspect_name,
            aspect_description=persona_aspect.aspect_description,
            backstory_id=backstory_id,
            strength_of_aspect_in_personality=persona_aspect.strength_of_aspect_in_personality
        )
