from dao.BaseDAO import BaseDAO
from entity.base import PersonaAspectConversationEntity


class PersonaAspectConversationDAO(BaseDAO):
    def __init__(self, db):
        super().__init__(db, PersonaAspectConversationEntity)

    def find_by_persona_id(self, persona_id):
        pass