from typing import List

from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import UniverseMetadataEntity


class UniverseMetadataDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, UniverseMetadataEntity)

    def find_by_universe_id(self, universe_id: int) -> List[UniverseMetadataEntity]:
        return self.db.query(UniverseMetadataEntity).filter_by(universe_id = universe_id).all()