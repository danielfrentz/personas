from typing import Optional

from pydantic import BaseModel


class PersonaFact(BaseModel):
    id: Optional[int] = None
    persona_id: Optional[int] = None
    fact: str
    fact_explanation: str