from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import SelfDescriptionConversationEntity


class SelfDescriptionConversationDao(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, SelfDescriptionConversationEntity)

    def find_by_persona_id(self, persona_id):
        return self.db.query(SelfDescriptionConversationEntity).filter(SelfDescriptionConversationEntity.persona_id == persona_id).all()