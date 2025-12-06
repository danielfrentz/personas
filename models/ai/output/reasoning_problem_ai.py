from typing import Optional

from pydantic import BaseModel, Field


class ReasoningProblemStatementAI(BaseModel):
    problem_statement: str = Field(
        description="The problem statement phrased as a user requesting that something be done.")
    problem_solution: str = Field(
        description="The solution to the problem statement phrased as a deliverable that is being created.")
    problem_solution_deliverable: Optional[str] = Field(
        description="The deliverable being delivered. Only necessary in cases where it is applicable, but must not be a reference, ie the text must be the thing being created. purely as examples: if the problem was prove a theorem, itd be the proof, if it was write an algorithm, itd be code. ", default=None)
