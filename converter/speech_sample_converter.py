from entity.base import SpeechSampleEntity
from models.ai.output.speech_sample_ai import SpeechSampleAI
from models.speech_sample import SpeechSample


class SpeechSampleConverter:
    def __init__(self):
        pass

    def model_to_entity(self, speech_sample: SpeechSample) -> SpeechSampleEntity:
        return SpeechSampleEntity(
            id=speech_sample.id,
            situation=speech_sample.situation,
            example=speech_sample.example,
            tone=speech_sample.tone,
            speech_profile_id=speech_sample.speech_profile_id,
            explanation=speech_sample.explanation,
            feeling=speech_sample.feeling
        )

    def entity_to_model(self, speech_sample_entity: SpeechSampleEntity) -> SpeechSample:
        return SpeechSample(
            id=speech_sample_entity.id,
            speech_profile_id=speech_sample_entity.speech_profile_id,
            situation=speech_sample_entity.situation,
            example=speech_sample_entity.example,
            tone=speech_sample_entity.tone,
            explanation=speech_sample_entity.explanation,
            feeling=speech_sample_entity.feeling
        )

    def ai_to_model(self, speech_sample_ai: SpeechSampleAI, speech_profile_id: int) -> SpeechSample:
        return SpeechSample(
            example=speech_sample_ai.example,
            situation=speech_sample_ai.situation,
            tone=speech_sample_ai.tone,
            speech_profile_id=speech_profile_id,
            explanation=speech_sample_ai.explanation,
            feeling=speech_sample_ai.feeling
        )