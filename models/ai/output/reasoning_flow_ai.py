from typing import List

from pydantic import BaseModel, Field

from models.reasoning_conversation import ReasoningRole


class ReasoningFlowAI(BaseModel):
    precise_problem_statement: str = Field(description="The precise problem statement")
    precise_problem_solution: str = Field(description="The precise problem solution.")
    persona_roles: List[ReasoningRole] = Field(description="The roles each persona will play in the conversation, the key is their precise name.")
    flow_description: List[str] = Field(description="The description of the conversation, stated in steps.")
