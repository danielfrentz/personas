from fastapi import APIRouter, Depends

from endpoint import get_speech_profile_service
from endpoint.rest.speech_sample import speech_sample_rest_router
from models.speech_profile import SpeechProfile
from service.persona_domain.speech_profile_service import SpeechProfileService

speech_profile_rest_router = APIRouter(prefix="/{persona_id}/speech_profile")
speech_profile_rest_router.include_router(speech_sample_rest_router)
@speech_profile_rest_router.put(path="/")
async def create(speech_profile: SpeechProfile, persona_id: int,
           speech_profile_service: SpeechProfileService = Depends(get_speech_profile_service)) -> SpeechProfile:
    return speech_profile_service.create(persona_id, speech_profile)

@speech_profile_rest_router.get(path="/speech_profile")
async def get(persona_id: int, speech_profile_service: SpeechProfileService = Depends(get_speech_profile_service)):
    return speech_profile_service.find_by_persona_id(persona_id)

@speech_profile_rest_router.delete(path="/{speech_profile_id}")
async def delete(speech_profile_id: int, speech_profile_service: SpeechProfileService = Depends(get_speech_profile_service)):
    return speech_profile_service.delete(speech_profile_id)