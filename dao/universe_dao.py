from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import UniverseEntity


class UniverseDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, UniverseEntity)

