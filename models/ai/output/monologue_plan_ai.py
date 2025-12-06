from typing import List

from pydantic import BaseModel, Field


class MonologuePlanAI(BaseModel):
    roles: dict[str, str] = Field(description="The roles each persona will play in the conversation, the key is their name while the value is the role they will play.")
    justification_that_final_turn_delivers_result: str = Field(description="A justification for why the final turn delivers the result.")
    dynamic: str = Field(description="The dynamic of how the people will interact with each other.")
    conversation_steps: List[str]