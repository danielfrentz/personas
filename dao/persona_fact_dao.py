from dao.BaseDAO import BaseDAO
from entity.base import PersonaFactEntity


class PersonaFactDAO(BaseDAO):
    def __init__(self, db):
        super().__init__(entity_type=PersonaFactEntity, db=db)

    def find_by_persona_id(self, persona_id):
        return self.db.query(PersonaFactEntity).filter(PersonaFactEntity.persona_id == persona_id).all()