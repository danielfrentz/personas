from dao.BaseDAO import BaseDAO
from entity.base import PersonaSkillEntity


class PersonaSkillDAO(BaseDAO):
    def __init__(self, db):
        super().__init__(db, PersonaSkillEntity)