from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import SpeechProfileEntity


class SpeechProfileDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, SpeechProfileEntity)

    def find_by_persona_id(self, persona_id):
        return self.db.query(SpeechProfileEntity).filter(SpeechProfileEntity.persona_id == persona_id).first()