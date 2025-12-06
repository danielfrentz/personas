from sqlalchemy import and_

from dao.BaseDAO import BaseDAO
from entity.base import PersonaAspectEntity


class PersonaAspectDao(BaseDAO):
    def __init__(self, db):
        super().__init__(db, PersonaAspectEntity)

    def find_by_persona_and_name(self, persona_id, aspect_name):
        return self.db.query(PersonaAspectEntity).filter(and_(PersonaAspectEntity.backstory_id == persona_id, PersonaAspectEntity.aspect_name==aspect_name)).first()

    def find_by_backstory_id(self, backstory_id):
        return self.db.query(PersonaAspectEntity).filter(PersonaAspectEntity.backstory_id == backstory_id).all()