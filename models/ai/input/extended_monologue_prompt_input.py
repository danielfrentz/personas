from pydantic import Field, BaseModel

from models.monologue import Monologue


class ExtendedMonologuePromptInput(BaseModel):
    base_monologue: Monologue = Field(description="The monologue from which this one should be based.")

