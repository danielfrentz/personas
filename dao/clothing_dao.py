from typing import List

from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import ClothingEntity


class ClothingDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, ClothingEntity)

    def find_by_physical_description_id(self, physical_description_id: int) -> List[ClothingEntity]:
        return self.db.query(ClothingEntity).filter(ClothingEntity.physical_description_id == physical_description_id).all()