from pydantic import BaseModel

from models.backstory import Backstory


class HobbyInput(BaseModel):
    backstory: Backstory
    