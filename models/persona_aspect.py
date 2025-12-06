from typing import Optional

from pydantic import BaseModel


class PersonaAspect(BaseModel):
    id: Optional[int] = None
    aspect_name: str
    aspect_description: str
    strength_of_aspect_in_personality: int
    backstory_id: int