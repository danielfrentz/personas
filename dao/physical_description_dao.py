from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import PhysicalDescriptionEntity


class PhysicalDescriptionDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, PhysicalDescriptionEntity)

    def find_by_id(self, physical_description_id):
        return self.db.query(PhysicalDescriptionEntity).filter(PhysicalDescriptionEntity.id == physical_description_id).first()

    def find_by_persona_id(self, persona_id):
        return self.db.query(PhysicalDescriptionEntity).filter(PhysicalDescriptionEntity.persona_id == persona_id).first()
