from typing import Optional


class AccessoryConversation:
    id: Optional[int] = None
    accessory_id: int
    wearer_id: int
    prompter_id: int