from pydantic import Field, BaseModel


class InitialRelationshipAI(BaseModel):
    relationship_type: str = Field(description="The relationship type that the source persona has with the target persona.")
    relationship_subtype: str = Field(description="The relationship subtype that the source persona has with the target persona. must be a subtype of the relationship_type.")
    relationship_description: str = Field(description="The overall description of the relationship that the source persona has with the target persona.")