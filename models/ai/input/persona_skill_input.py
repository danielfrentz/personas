from pydantic import BaseModel

from models.backstory import Backstory


class SkillInput(BaseModel):
    backstory: Backstory