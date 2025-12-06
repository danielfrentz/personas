from entity.base import PersonaSkillEntity
from models.ai.output.persona_skill_ai import PersonaSkillAI
from models.persona_skill import PersonaSkill


class PersonaSkillConverter:
    def model_to_entity(self, skill: PersonaSkill) -> PersonaSkillEntity:
        return PersonaSkillEntity(
            skill_name=skill.skill_name,
            skill_description=skill.skill_description,
            persona_id=skill.persona_id,
            id=skill.id
        )

    def entity_to_model(self, skill_entity: PersonaSkillEntity) -> PersonaSkill:
        return PersonaSkill(
            skill_name=skill_entity.skill_name,
            skill_level=skill_entity.skill_level,
            skill_description=skill_entity.skill_description,
            persona_id=skill_entity.persona_id,
            id=skill_entity.id
        )

    def ai_to_model(self, skill_ai: PersonaSkillAI, persona_id: int) -> PersonaSkill:
        return PersonaSkill(
            skill_name=skill_ai.skill_name,
            skill_level=skill_ai.skill_level,
            skill_description=skill_ai.skill_description,
            persona_id=persona_id,

        )