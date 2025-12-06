from pydantic import BaseModel


class PersonaSkillAI(BaseModel):
    skill_type: str
    skill_source: str
    skill_name: str
    skill_description: str
    skill_level: str
