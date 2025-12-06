from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import PromptPerformanceEntity


class PromptPerformanceDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, PromptPerformanceEntity)