from fastapi import APIRouter, Depends

from endpoint import get_life_events_service
from endpoint.rest.story import story_rest_router
from models.life_event import LifeEvent
from service.persona_domain.life_event_service import LifeEventService

life_event_rest_router = APIRouter(prefix="/{persona_id}/life_events")
life_event_rest_router.include_router(story_rest_router)
@life_event_rest_router.post("/")
async def create_life_event(life_event: LifeEvent,
                            persona_id: int,
                            life_event_service: LifeEventService = Depends(get_life_events_service)) -> LifeEvent:
    return life_event_service.create(life_event, persona_id)

@life_event_rest_router.get("/{life_event_id}/")
async def get_by_id(life_event_id: int, life_event_service: LifeEventService = Depends(get_life_events_service)):
    return life_event_service.find_by_id(life_event_id)

@life_event_rest_router.get("/")
async def get_all(persona_id: int, life_event_service: LifeEventService = Depends(get_life_events_service)):
    return life_event_service.find_by_persona_id(persona_id=persona_id)

@life_event_rest_router.delete("/{life_event_id}")
async def delete(life_event_id: int, life_event_service: LifeEventService = Depends(get_life_events_service)):
    return life_event_service.delete(life_event_id)