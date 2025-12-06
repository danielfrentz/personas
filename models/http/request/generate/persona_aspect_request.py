from pydantic import BaseModel


class PersonaAspectRequest(BaseModel):
    aspect_name: str