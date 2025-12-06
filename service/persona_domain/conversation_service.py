from converter.conversation_converter import ConversationConverter
from dao.conversation_dao import ConversationDAO
from models.conversation import Conversation


class ConversationService:
    """

    """
    def __init__(self, conversation_dao: ConversationDAO, conversation_converter: ConversationConverter):
        self.conversation_dao = conversation_dao
        self.conversation_converter = conversation_converter

    def find_by_id(self, conversation_id: int) -> Conversation:
        conversation_entity = self.conversation_dao.find_by_id(conversation_id)
        return self.conversation_converter.entity_to_model(conversation_entity)

    def find_by_source_id(self, source_id: int, source: str) -> Conversation:
        habit_entity = self.conversation_dao.find_by_id_and_source(source_id, source)
        return self.conversation_converter.entity_to_model(habit_entity)

    def save(self, conversation: Conversation, source_id: int, source_name: str) -> Conversation:
        conversation.source_name = source_name
        conversation.source_id = source_id
        conversation_entity = self.conversation_converter.model_to_entity(conversation)
        conversation_entity = self.conversation_dao.save(conversation_entity)
        return self.conversation_converter.entity_to_model(conversation_entity)

    def delete(self, conversation_id: int):
        self.conversation_dao.delete(conversation_id)
