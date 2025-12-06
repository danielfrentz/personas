from typing import List

from fastapi import APIRouter, Depends

from endpoint import get_speech_sample_service
from models.speech_sample import SpeechSample
from service.persona_domain.speech_sample_service import SpeechSampleService

speech_sample_rest_router = APIRouter(prefix="/sample")

@speech_sample_rest_router.post("/")
async def create(speech_sample_model: SpeechSample, speech_sample_service: SpeechSampleService = Depends(get_speech_sample_service)) -> SpeechSample:
    return speech_sample_service.save(speech_sample_model)
@speech_sample_rest_router.get("/")
async def get_all(persona_id: int, speech_sample_service: SpeechSampleService = Depends(get_speech_sample_service)) -> List[SpeechSample]:
    return speech_sample_service.get_by_persona_id(persona_id=persona_id)
@speech_sample_rest_router.delete("/{speech_sample_id}")
async def delete_speech_sample(speech_sample_id: int, speech_sample_service: SpeechSampleService = Depends(get_speech_sample_service)):
    return speech_sample_service.delete(speech_sample_id)

@speech_sample_rest_router.delete("/")
async def delete_speech_samples_by_persona_id(persona_id: int, speech_sample_service: SpeechSampleService = Depends(get_speech_sample_service)):
    speech_sample_service.delete_by_persona_id(persona_id=persona_id)

