from typing import List

from converter.speech_sample_converter import SpeechSampleConverter
from dao.speech_sample_dao import SpeechSampleDAO
from models.ai.input.speech_sample_input import SpeechSampleInput
from models.ai.output.speech_sample_ai import SpeechSampleAI
from models.speech_sample import SpeechSample
from service.ai.ai_service import AIService
from service.persona_domain.persona_service import PersonaService


class SpeechSampleService:
    def __init__(self, speech_sample_dao: SpeechSampleDAO,
                 speech_sample_converter: SpeechSampleConverter,
                 ai_service: AIService,
                 persona_service: PersonaService,):
        self.speech_sample_dao = speech_sample_dao
        self.speech_sample_converter = speech_sample_converter
        self.ai_service = ai_service
        self.persona_service = persona_service

    def generate(self, persona_id: int, universe_id: int) -> SpeechSample:
        persona = self.persona_service.find_by_id(persona_id)
        speech_sample_input = SpeechSampleInput(
            backstory=persona.backstory,
            speech_profile=persona.speech_profile
        )
        generated_sample = self.ai_service.call_llm(system_prompt_name="create_speech_sample", return_type=SpeechSampleAI, user_data=speech_sample_input, universe_id=universe_id, validator=self.create_validation(persona.speech_profile.samples))
        return self.speech_sample_converter.ai_to_model(generated_sample, speech_profile_id=persona.speech_profile.id)

    def get_by_persona_id(self, persona_id: int):
        return self.persona_service.find_by_id(persona_id).speech_profile.samples

    def get_by_speech_profile_id(self, speech_profile_id: int) -> List[SpeechSample]:
        speech_sample_entities = self.speech_sample_dao.find_by_speech_profile_id(speech_profile_id)
        return [self.speech_sample_converter.entity_to_model(sample) for sample in speech_sample_entities]

    def save(self, speech_sample: SpeechSample) -> SpeechSample:
        speech_sample_entity = self.speech_sample_converter.model_to_entity(speech_sample)
        speech_sample_entity.speech_profile_id = speech_sample.speech_profile_id
        self.speech_sample_dao.save(speech_sample_entity)
        return self.speech_sample_converter.entity_to_model(speech_sample_entity)

    def create_validation(self, all_samples: List[SpeechSample]):
        def validation(speech_sample: SpeechSample):
            prefix = speech_sample.example[:50]
            if len([sample for sample in all_samples if sample.example.startswith(prefix)]) > 0:
                raise ValueError("The example must be unique from the other samples to ensure diversity.")
        return validation

    def find_by_id(self, entity_id: int) -> SpeechSample:
        speech_sample_entity = self.speech_sample_dao.find_by_id(entity_id)
        return self.speech_sample_converter.entity_to_model(speech_sample_entity)

    def delete(self, entity_id: int):
        self.speech_sample_dao.delete(entity_id)

    def delete_by_persona_id(self, persona_id):
        speech_profile_id = self.persona_service.find_by_id(persona_id).speech_profile.id
        self.speech_sample_dao.delete_by_persona_id(speech_profile_id=speech_profile_id)
