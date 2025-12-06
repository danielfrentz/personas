from pydantic import BaseModel, Field


class MonologuePromptAI(BaseModel):
    prompt_text: str = Field(description="The text that the user speaks to start the conversation.")