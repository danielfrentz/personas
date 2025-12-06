from pydantic import BaseModel

from models.backstory import Backstory


class HabitsInput(BaseModel):
    backstory: Backstory

