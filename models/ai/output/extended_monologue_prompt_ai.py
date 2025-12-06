from pydantic import BaseModel, Field


class ExtendedMonologuePromptAI(BaseModel):
    prompt_text: str = Field(description="The text that the user speaks to start the conversation.")
    reason_for_followup: str