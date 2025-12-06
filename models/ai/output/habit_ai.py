from pydantic import BaseModel, Field

from models.ai.output.conversation_ai import ConversationAI


class HabitAI(BaseModel):
    habit_name: str = Field(description="The name of a habit this person has.")
    frequency: str = Field(description="The frequency of the habit.")
    internal_monologue: ConversationAI = Field(description="An internal monologue of the persona realizing they have this habit.")
    description: str = Field(description="A description of the habit.")
    good_habit: bool = Field(description="Whether the persona thinks this is a good habit.")