from typing import List

from pydantic import BaseModel

from models.backstory import Backstory
from models.conversation import Conversation
from models.memory import Memory
from models.story import Story


class MemoryInput(BaseModel):
    backstory: Backstory
    recent_memories: List[Memory]
    story: Story
    conversation: Conversation