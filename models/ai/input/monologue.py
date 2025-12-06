from typing import List

from pydantic import BaseModel, Field

from models.ai.output.monologue_plan_ai import MonologuePlanAI
from models.persona import Persona


class MonologueInput(BaseModel):
    prompt: str = Field(description="The text that the user spoke to start the conversation.")
    speakers: List[Persona] = Field(description="The speaker in the conversation. This is the only one that should speak after the first prompt.")
    monologue_plan: MonologuePlanAI = Field(description="The overall flow of the conversation. Must be followed.")
    custom_instructions: List[str] = Field(description="Additional instructions that the user wants to add to guide the monologue plan.")
    problem_type: str = Field(description="The type of problem that the user wants to solve.")
    minimum_turns: int = Field(description="The minimum number of turns that the monologue should have.")
