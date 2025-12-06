from typing import List, Optional, Dict

from pydantic import BaseModel, Field

from models.ai.input.reasoning_participant import ReasoningParticipant
from models.backstory import Backstory
from models.conversation import Conversation


class ReasoningRole(BaseModel):
    role_description: str
    debate_style: str
    name: str = Field(description="The name of the persona")

class ReasoningTopicInput(BaseModel):
    previous_topics: List[str]
    persona_name: str
    persona_description: str

class ReasoningConversation(BaseModel):
    id: Optional[int] = None
    conversation: Conversation
    problem_statement: str
    persona_id: int
    extends_id: Optional[int] = None
    theme: Optional[str] = Field(default=None)

class ReasoningTopic(BaseModel):
    reasoning_topic: str


class ReasoningFlowInput(BaseModel):
    topic: str
    problem_presenter: Backstory
    possible_participants: Dict[str, ReasoningParticipant]
    answer_expectation: str
    error_made: bool = Field(default=False)
    problem_statement: Optional[str] = None
    solution: Optional[str] = None

class ExtendedReasoningFlowInput(BaseModel):
    topic: str
    problem_presenter: Backstory
    possible_participants: Dict[str, ReasoningParticipant]
    previous_problem: ReasoningConversation


