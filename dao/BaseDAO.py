from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from entity.base import Base


class BaseDAO:

    def __init__(self, db: Session, entity_type: Type[Base]):
        self.db = db
        self.entity_type = entity_type


    def delete(self, entity_id: int) -> None:
        entity = self.find_by_id(entity_id)
        self.db.delete(entity)
        self.db.commit()

    def save(self, entity: Base):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Base, entity_id: int):
        entity.id = entity_id
        self.db.merge(entity)
        self.db.commit()
        return entity

    def find_by_id(self, entity_id: int):
        try:
            return self.db.query(self.entity_type).filter(self.entity_type.id == entity_id).first()
        except Exception:
            raise HTTPException(status_code=404, detail="Entity not found of type {self.entity_type.name} with id {entity_id}")

    def find_all(self):
        return self.db.query(self.entity_type).all()

    def exists(self, universe_id):
        return self.db.query(self.entity_type).filter(self.entity_type.id == universe_id).scalar()
