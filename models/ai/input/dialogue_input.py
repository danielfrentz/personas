from pydantic import BaseModel

from models.backstory import Backstory


class DialogueInput(BaseModel):
    prompter: Backstory
    conversation_partner: Backstory
    