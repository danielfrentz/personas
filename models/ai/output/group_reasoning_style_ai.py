from pydantic import BaseModel, Field


class GroupReasoningStyleAI(BaseModel):
    assumed_role: str = Field(description="The role this person typically plays in group problems.")
    tone: str = Field(description="What tone do they use for most of the conversation. More specifics can be given in style description.")
    devils_advocate: bool = Field(description="is this person a devils advocate when reasoning in a group?")
    sarcastic: bool = Field(description="is this person sarcastic when reasoning in a group?")
    reserved: bool = Field(description="is this person reserved with their opinions when reasoning in a group?")
    witty: bool = Field(description="is this person witty when reasoning in a group?")
    subtle: bool = Field(description="is this person subtle when reasoning in a group?")
    style_description: str = Field(description="A general description of how this person performs within a group when reasoning through a problem.")
