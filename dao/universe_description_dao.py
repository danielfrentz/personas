from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import UniverseDescriptionEntity


class UniverseDescriptionDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, UniverseDescriptionEntity)

    def find_by_universe_id(self, universe_id: int) -> UniverseDescriptionEntity:
        return self.db.query(UniverseDescriptionEntity).filter(UniverseDescriptionEntity.universe_id == universe_id).first()

