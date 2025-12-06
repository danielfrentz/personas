from typing import List, Optional

from pydantic import BaseModel, Field

from models.habit import Habit
from models.hobby import Hobby
from models.like import Like
from models.persona_aspect import PersonaAspect
from models.persona_knowledge import PersonaKnowledge
from models.persona_skill import PersonaSkill


class Backstory(BaseModel):
    id: Optional[int] = None
    name: str
    persona_id: Optional[int] = None
    place_of_birth: str
    date_of_birth: str
    description: str
    education_description: str
    social_description: str
    historical: Optional[bool] = False
    gender: str
    habits: List[Habit]
    hobbies: List[Hobby] = Field(default_factory=list)
    likes: Optional[List[Like]] = Field(default_factory=list)
    skills: Optional[List[PersonaSkill]] = Field(default_factory=list)
    knowledge: Optional[List[PersonaKnowledge]] = Field(default_factory=list)
    aspects: Optional[List[PersonaAspect]] = Field(default_factory=list)
