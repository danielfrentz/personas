from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import StoryEntity


class StoryDAO(BaseDAO):

    def __init__(self, db: Session):
        super().__init__(db, StoryEntity)

    def find_by_life_event_id(self, life_event_id):
        return self.db.query(StoryEntity).filter(StoryEntity.life_event_id == life_event_id).all()

