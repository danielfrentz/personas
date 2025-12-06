from typing import Optional

from pydantic import BaseModel

from models.backstory import Backstory
from models.physical_description import PhysicalDescription


class SpeechProfileInput(BaseModel):
    backstory: Backstory
    physical_description: PhysicalDescription
    emojis_allowed: Optional[bool] = False
    verbose: Optional[bool] = False