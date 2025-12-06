from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import MemoryEntity


class MemoryDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, MemoryEntity)

    def find_by_story_id(self, story_id):
        return self.db.query(MemoryEntity).filter(MemoryEntity.story_id == story_id).all()

    def find_by_conversation_id(self, conversation_id):
        return self.db.query(MemoryEntity).filter(MemoryEntity.story_id == story_id).all()
