from typing import List

from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import IntrospectionEntity


class IntrospectionDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, IntrospectionEntity)

    def find_by_story_id(self, story_id) -> List[IntrospectionEntity]:
        return self.db.query(IntrospectionEntity).filter(IntrospectionEntity.story_id == story_id).all()
