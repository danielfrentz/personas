from typing import Optional

from pydantic import BaseModel

from models.conversation import Conversation


class Interview(BaseModel):
    id: Optional[int] = None
    interviewer_id: int
    interviewee_id: int
    interview_topic: str
    interview_conversation: Conversation