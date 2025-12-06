from pydantic import Field, BaseModel


class LikeAI(BaseModel):
    what_this_like_dislike_pair_teaches_about_the_person: str
    why_this_like_is_unique_to_the_existing_likes: str
    why_this_dislike_is_unique_to_the_existing_likes: str
    personality_aspect_like_appeals_to: str
    personality_aspect_dislike_appeals_to: str
    like_name: str = Field(description="Name of the thing the person likes.")
    like_reason: str = Field(description="Reason why they like this thing.")
    dislike_name: str = Field(description="Name of the thing the person dislikes.")
    dislike_reason: str = Field(description="Reason why they dislike this thing.")
    why_outsider_sees_as_contradiction: str = Field(description="A possible contradiction in their like and dislike.")
    contradiction_explanation: str = Field(description="Explanation for why this is not a contradiction.")