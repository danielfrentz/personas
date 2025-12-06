from typing import List

from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import PersonaRelationshipEntity


class RelationshipDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, PersonaRelationshipEntity)

    def find_by_persona_id(self, persona_id) -> List[PersonaRelationshipEntity]:
        return self.db.query(PersonaRelationshipEntity).filter(PersonaRelationshipEntity.id == persona_id).all()

    def find_by_id_source_target(self, source_id, target_id):
        return self.db.query(PersonaRelationshipEntity).filter(PersonaRelationshipEntity.source_id == source_id, PersonaRelationshipEntity.target_id == target_id).first()
