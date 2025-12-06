from typing import Dict, List

from pydantic import BaseModel

from models.ai.input.reasoning_participant import ReasoningParticipant
from models.ai.output.reasoning_flow_ai import ReasoningFlowAI
from models.ai.output.reasoning_problem_ai import ReasoningProblemStatementAI
from models.backstory import Backstory
from models.reasoning_conversation import ReasoningConversation


class ReasoningConversationInput(BaseModel):
    conversation_flow: ReasoningFlowAI
    participants: Dict[str, ReasoningParticipant]
    problem_statement: ReasoningProblemStatementAI

class ExtendedReasoningConversationInput(BaseModel):
    conversation_flow: ReasoningFlowAI
    participants: Dict[str, ReasoningParticipant]
    previous_problem: ReasoningConversation

class ReasoningProblemInput(BaseModel):
    theme: str
    universe_description: str
    problem_presenter: Backstory
    previous_problems: List[str]

class ExtendedReasoningProblemInput(BaseModel):
    problem_presenter: Backstory
    previous_problem: ReasoningConversation