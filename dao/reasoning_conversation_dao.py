from typing import List

from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import ReasoningConversationEntity


class ReasoningConversationDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, ReasoningConversationEntity)

    def find_by_persona(self, persona_id):
        return self.db.query(ReasoningConversationEntity).filter(ReasoningConversationEntity.persona_id == persona_id).all()

    def find_previous(self, theme) -> List[ReasoningConversationEntity]:
        return self.db.query(ReasoningConversationEntity).filter(ReasoningConversationEntity.theme == theme).all()