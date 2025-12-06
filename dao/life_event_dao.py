from typing import List

from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import LifeEventEntity


class LifeEventDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, LifeEventEntity)

    def find_by_persona_id(self, persona_id: int) -> List[LifeEventEntity]:
        return self.db.query(LifeEventEntity).filter(LifeEventEntity.persona_id == persona_id)

