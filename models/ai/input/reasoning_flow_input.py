from typing import List

from pydantic import BaseModel

from models.backstory import Backstory


class ReasoningFlowInput(BaseModel):
    problem_statement: str
    possible_participants: List[Backstory]