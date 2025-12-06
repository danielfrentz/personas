import logging

from sqlalchemy.orm import Session

from dao.BaseDAO import BaseDAO
from entity.base import SpeechSampleEntity, StoryEntity


class SpeechSampleDAO(BaseDAO):
    def __init__(self, db: Session):
        super().__init__(db, StoryEntity)
        self.logger = logging.getLogger(__name__)

    def find_by_speech_profile_id(self, speech_profile_id: int):
        return self.db.query(SpeechSampleEntity).filter_by(speech_profile_id=speech_profile_id).all()

    def delete_by_persona_id(self, speech_profile_id: int):
        self.logger.info(f"Deleting speech samples for speech profile id: {speech_profile_id}")
        return self.db.query(SpeechSampleEntity).filter_by(speech_profile_id=speech_profile_id).delete()


