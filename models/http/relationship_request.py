from pydantic import BaseModel


class RelationshipRequest(BaseModel):
    source_persona_id: int
    target_persona_id: int