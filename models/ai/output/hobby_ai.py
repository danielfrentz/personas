from pydantic import BaseModel, Field


class HobbyAI(BaseModel):
    name: str = Field(description="The name of the hobby.")
    description: str = Field(description="The details of the persons interest in this hobby.")