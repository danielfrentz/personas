from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import HobbyEntity


class HobbyDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(entity_type=HobbyEntity, db=db)

    def find_by_backstory_id(self, backstory_id):
        return self.db.query(HobbyEntity).filter(HobbyEntity.backstory_id == backstory_id).all()