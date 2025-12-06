from converter.speech_profile_converter import SpeechProfileConverter
from dao.speech_profile_dao import SpeechProfileDAO
from models.ai.input.speech_profile_input import SpeechProfileInput
from models.ai.output.speech_profile_ai import SpeechProfileAI
from models.http.request.generate.speech_profile_request import SpeechProfileRequest
from models.speech_profile import SpeechProfile
from service.ai.ai_service import AIService
from service.persona_domain.persona_service import PersonaService


class SpeechProfileService:

    def __init__(self, ai_service: AIService,
                 speech_dao: SpeechProfileDAO,
                 speech_profile_converter: SpeechProfileConverter,
                 persona_service: PersonaService):
        self.ai_service = ai_service
        self.speech_dao = speech_dao
        self.persona_service = persona_service
        self.speech_profile_converter = speech_profile_converter
        self.persona_service = persona_service

    def generate(self, persona_id: int, universe_id: int, speech_profile_request: SpeechProfileRequest) -> SpeechProfile:
        persona = self.persona_service.find_by_id(persona_id)
        speech_input = SpeechProfileInput(
            backstory=persona.backstory,
            physical_description=persona.physical_description,
            verbose=speech_profile_request.verbose,
            emojis_allowed=speech_profile_request.emojis_allowed
        )
        generated_profile: SpeechProfileAI = self.ai_service.call_llm(system_prompt_name="create_speech_profile", return_type=SpeechProfileAI, user_data=speech_input, universe_id=universe_id)

        result = self.speech_profile_converter.ai_to_model(generated_profile)
        result.emojis_allowed = speech_profile_request.emojis_allowed
        result.verbose = speech_profile_request.verbose
        return result

    def create(self, persona_id: int, speech_profile: SpeechProfile):
        speech_profile_entity = self.speech_profile_converter.model_to_entity(speech_profile)
        speech_profile_entity.persona_id = persona_id
        self.speech_dao.save(speech_profile_entity)
        return self.speech_profile_converter.entity_to_model(speech_profile_entity)

    def find_by_persona_id(self, persona_id):
        speech_entity = self.speech_dao.find_by_persona_id(persona_id)
        return self.speech_profile_converter.entity_to_model(speech_entity)

    def delete(self, speech_profile_id):
        self.speech_dao.delete(speech_profile_id)
