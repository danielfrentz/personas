from typing import List

from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import BackstoryEntity


class BackstoryDAO(BaseDAO):

    def __init__(self, db: Session):
        super().__init__(db, BackstoryEntity)

    def get_all(self) -> List[BackstoryEntity]:
        return self.db.query(BackstoryEntity).all()

    def find_by_persona_id(self, persona_id: int) -> BackstoryEntity:
        return self.db.query(BackstoryEntity).filter(BackstoryEntity.persona_id == persona_id).first()

    def find_by_persona_name(self, name) -> BackstoryEntity:
        return self.db.query(BackstoryEntity).filter(BackstoryEntity.persona.habit_name == name).first()

    def find_by_universe(self, universe_id) -> List[BackstoryEntity]:
        return self.db.query(BackstoryEntity).filter(BackstoryEntity.persona.universe_id == universe_id).all()