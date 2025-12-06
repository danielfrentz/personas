import logging
from typing import List

from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import MonologueEntity

logger = logging.getLogger(__name__)

class MonologueDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, MonologueEntity)

    def find_by_theme(self, theme) -> List[MonologueEntity]:
        return self.db.query(MonologueEntity).filter(MonologueEntity.theme == theme).all()

    def find_by_speaker_id(self, speaker_id) -> List[MonologueEntity]:
        return self.db.query(MonologueEntity).filter(MonologueEntity.speaker_id == speaker_id).all()

    def search(self, persona_id, themes):
        query = self.db.query(MonologueEntity)
        if persona_id:
            logger.debug("querying by persona_id {persona_id}".format(persona_id=persona_id))
            query = query.filter(MonologueEntity.speaker_id == persona_id)

        return query.all()