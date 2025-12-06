from typing import Optional

from pydantic import BaseModel, Field


class ConversationTurnAI(BaseModel):
    speaker: str = Field(description="The person who is speaking during this turn.")
    action: Optional[str] = Field(description="An optional field which can be used to state single action.", default=None)
    tone: str = Field(description="The tone that the persona is using as they utter the text.")
    directed_at: list[str] = Field(description="The person who the text is directed at, use everyone when speaking to everyone. Always just the name.", min_length=1)
    feeling: str = Field(description="The feeling that the persona is having during this turn.")
    text: str = Field(
        description="Based on the speech profile of the speaker, the exact way in which it is specified will be determined by how this person interacts with the person they are directing it at. The wording should reflect the action tone and feeling if these are also present")
    private_thought: str
    turn_purpose: str