from pydantic import BaseModel


class RelationshipFeelingAI(BaseModel):
    feeling_name: str
    reason: str