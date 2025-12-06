from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import HairStyleEntity


class HairStyleDAO(BaseDAO):
    def __init__(self, db_session: Session):
        super().__init__(db=db_session, entity_type=HairStyleEntity)
