from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import LikesEntity


class LikeDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, LikesEntity)

    def find_by_persona_id(self, backstory_id: int):
        return self.db.query(self.entity_type).filter(LikesEntity.backstory_id == backstory_id).all()
