from typing import List

from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import UniverseLocationEntity


class UniverseLocationDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, UniverseLocationEntity)

    def get_by_universe(self, universe_id: int) -> List[UniverseLocationEntity]:
        return self.db.query(UniverseLocationEntity).filter_by(universe_id=universe_id).all()