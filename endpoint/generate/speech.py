from fastapi import APIRouter, Depends

from endpoint import get_speech_profile_service
from endpoint.generate.speech_sample import speech_sample_generate_router
from models.http.request.generate.speech_profile_request import SpeechProfileRequest
from models.speech_profile import SpeechProfile
from service.persona_domain.speech_profile_service import SpeechProfileService

speech_profile_generate_router = APIRouter(prefix="/{persona_id}/speech_profile")
speech_profile_generate_router.include_router(speech_sample_generate_router)
@speech_profile_generate_router.post("/")
async def generate_speech_profile(speech_profile_request: SpeechProfileRequest,
                            persona_id: int,
                            universe_id: int,
                            speech_profile_service: SpeechProfileService = Depends(get_speech_profile_service)) -> SpeechProfile:
    return speech_profile_service.generate(persona_id=persona_id, universe_id=universe_id, speech_profile_request=speech_profile_request)