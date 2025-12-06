from pydantic import BaseModel


class ObjectivePersonaRequest(BaseModel):
    name: str