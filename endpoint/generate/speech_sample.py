from fastapi import APIRouter, Depends

from endpoint import get_speech_sample_service
from service.persona_domain.speech_sample_service import SpeechSampleService

speech_sample_generate_router = APIRouter(prefix='/sample')
@speech_sample_generate_router.post("/")
async def generate(persona_id: int, universe_id: int, speech_sample_service: SpeechSampleService = Depends(get_speech_sample_service)):
    return speech_sample_service.generate(persona_id=persona_id, universe_id=universe_id)

