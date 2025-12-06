from models.conversation import Conversation


class RelationshipConversation:
    source_persona_id: int
    target_persona_id: int
    conversation: Conversation