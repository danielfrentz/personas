from fastapi import APIRouter, Depends

from endpoint import get_monologue_service, get_extended_monologue_service
from models.http.request.generate.monologue import MonologuePromptRequest
from models.monologue import Monologue
from service.persona_domain.extended_monologue_service import ExtendedMonologueService
from service.persona_domain.monologue_service import MonologueService

monologue_generate_router = APIRouter(prefix="/{universe_id}/monologue")

@monologue_generate_router.post("/", response_model=Monologue)
async def generate(monologue_request: MonologuePromptRequest, universe_id: int, monologue_service: MonologueService = Depends(get_monologue_service)):
    return monologue_service.generate(monologue_request=monologue_request, universe_id=universe_id)

@monologue_generate_router.post("/{monologue_id}/", response_model=Monologue)
async def generate_extended(monologue_id: int, universe_id: int, extended_monologue_service: ExtendedMonologueService = Depends(get_extended_monologue_service)) -> Monologue:
    return extended_monologue_service.generate(monologue_id=monologue_id, universe_id=universe_id)
