from typing import Optional

from pydantic import BaseModel


class PersonaSkill(BaseModel):
    skill_name: str
    skill_description: str
    skill_level: str
    persona_id: int
    id: Optional[int] = None
