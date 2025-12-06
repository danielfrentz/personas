from typing import List

from pydantic import BaseModel

from models.backstory import Backstory
from models.monologue import Monologue


class MonologuePromptInput(BaseModel):
    theme: str
    intent: str
    previous_prompts: List[str]
    backstory: Backstory
    custom_prompt_requirements: List[str]
    prompt_type: str

class ExtendedMonologuePromptInput(BaseModel):
    theme: str
    previous_monologue: Monologue