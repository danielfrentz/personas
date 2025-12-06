from typing import List, Optional

from pydantic import BaseModel, Field

from models.ai.output.monologue_prompt import MonologuePromptAI
from models.persona import Persona


class MonologuePlanInput(BaseModel):
    prompt: MonologuePromptAI = Field(description="The prompt that the question asker gave to start the conversation.")
    responders: List[Persona] = Field(description="A detailed description of the person who will be delivering the monologue.")
    prompter: Persona
    custom_instructions: List[str] = Field(description="Additional instructions that the user wants to add to guide the monologue plan.")
    make_mistake: bool = Field(description="Whether the user wants to make a mistake.")
    intent: str
    solution: Optional[str] = Field(description="The solution to the monologue plan.")
    include_examples: bool
    include_counter_examples: bool
    disagreement: bool
    problem_type: Optional[str] = None
    minimum_turns: int = Field(description="The minimum number of turns that the monologue should have.")