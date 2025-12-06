from fastapi import APIRouter, Depends

from endpoint import get_life_events_service
from endpoint.generate.story import story_generate_router
from models.http.request.generate.life_event_request import LifeEventRequest
from service.persona_domain.life_event_service import LifeEventService

life_event_generate_router = APIRouter(prefix="/{persona_id}/life_events")

life_event_generate_router.include_router(story_generate_router)
@life_event_generate_router.post(path="/")
async def generate_life_events(persona_id: int,
                        life_event_request: LifeEventRequest,
                         life_event_service: LifeEventService = Depends(get_life_events_service)):
    return life_event_service.generate(persona_id=persona_id, life_event_request=life_event_request)