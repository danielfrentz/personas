from typing import Optional

from pydantic import BaseModel, Field


class Like(BaseModel):
    id: Optional[int] = None
    backstory_id: int
    like_name: str = Field(description="Name of the thing the person likes.")
    like_reason: str = Field(description="Reason why they like this thing.")
    dislike_name: str = Field(description="Name of the thing the person dislikes.")
    dislike_reason: str = Field(description="Reason why they dislike this thing.")
    contradiction: str = Field("A possible contradiction in their like and dislike.")
    contradiction_explanation: str = Field(description="Explanation for why this is not a contradiction.")