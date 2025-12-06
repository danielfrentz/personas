from converter.speech_sample_converter import SpeechSampleConverter
from entity.base import SpeechProfileEntity
from models.ai.output.speech_profile_ai import SpeechProfileAI
from models.speech_profile import SpeechProfile


class SpeechProfileConverter:

    def __init__(self,
                 speech_sample_converter: SpeechSampleConverter):
        self.speech_sample_converter = speech_sample_converter

    def model_to_entity(self, speech_profile: SpeechProfile) -> SpeechProfileEntity | None:
        if speech_profile is None:
            return None
        samples = [self.speech_sample_converter.model_to_entity(sample) for sample in speech_profile.samples]
        result = SpeechProfileEntity(
            id=speech_profile.id,
            description=speech_profile.description,
            emotional_description=speech_profile.emotional_description,
            emojis_allowed = speech_profile.emojis_allowed,
            verbose=speech_profile.verbose
        )
        result.samples = samples
        return result

    def entity_to_model(self, speech_profile_entity: SpeechProfileEntity) -> SpeechProfile | None:
        if speech_profile_entity is None:
            return None
        samples = [self.speech_sample_converter.entity_to_model(sample) for sample in speech_profile_entity.samples]
        result = SpeechProfile(
            description=speech_profile_entity.description,
            id=speech_profile_entity.id,
            samples=samples,
            emotional_description=speech_profile_entity.emotional_description,
            emojis_allowed=speech_profile_entity.emojis_allowed,
            verbose=speech_profile_entity.verbose

        )
        return result

    def ai_to_model(self, speech_profile_ai: SpeechProfileAI) -> SpeechProfile:
        return SpeechProfile(
            description=speech_profile_ai.speech_description,
            emotional_description=speech_profile_ai.emotional_description
        )

    def model_to_ai(self, speech_profile_model: SpeechProfile) -> SpeechProfileAI:
        return SpeechProfileAI(
            speech_description=speech_profile_model.description,
            emotional_description=speech_profile_model.emotional_description
        )