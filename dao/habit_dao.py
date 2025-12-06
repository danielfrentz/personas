from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import HabitEntity


class HabitDAO(BaseDAO):
    def __init__(self, db_session: Session):
        super().__init__(db=db_session, entity_type=HabitEntity)

    def find_by_persona(self, backstory_id):
        return self.db.query(HabitEntity).filter(HabitEntity.backstory_id == backstory_id).all()