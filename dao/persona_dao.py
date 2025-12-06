from typing import List

from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import PersonaEntity


class PersonaDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, PersonaEntity)

    def get_persona_by_name(self, persona_name: str) -> PersonaEntity:
        return self.db.query(PersonaEntity).filter(PersonaEntity.name == persona_name).first()

    def get_existing_persona(self, universe_id) -> List[PersonaEntity]:
        return self.db.query(PersonaEntity).filter_by(universe_id = universe_id).all()