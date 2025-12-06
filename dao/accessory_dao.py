from typing import List

from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import AccessoryEntity


class AccessoryDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, AccessoryEntity)

    def get_by_physical_description_id(self, physical_description_id: int) -> List[AccessoryEntity]:
        return self.db.query(AccessoryEntity).filter_by(physical_description_id=physical_description_id).all()
