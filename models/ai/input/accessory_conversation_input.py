from pydantic import BaseModel

from models.accessory import Accessory
from models.backstory import Backstory


class AccessoryConversationInput(BaseModel):
    prompter_backstory: Backstory
    wearer_backstory: Backstory
    accessory: Accessory