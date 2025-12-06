from pydantic import BaseModel


class RawPersonaDescriptionResponse(BaseModel):
    description: str