from sqlalchemy import and_
from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import ConversationEntity


class ConversationDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, ConversationEntity)

    def save(self, conversation: ConversationEntity) -> ConversationEntity:
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def find_by_id_and_source(self, source_id: int, source: str) -> ConversationEntity:
        return self.db.query(ConversationEntity).filter(and_(ConversationEntity.source_id==source_id, ConversationEntity.source == source)).first()
