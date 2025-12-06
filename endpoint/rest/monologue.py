from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from endpoint import get_monologue_service
from models.monologue import Monologue
from service.persona_domain.monologue_service import MonologueService

monologue_rest_router = APIRouter(prefix="/{universe_id}/monologue")

@monologue_rest_router.get("/{monologue_id}")
async def get(monologue_id: int, monologue_service: MonologueService = Depends(get_monologue_service)) -> Monologue:
    return monologue_service.find_by_id(monologue_id)

@monologue_rest_router.get("/")
async def search(universe_id: int, persona_id: int = Query(None), themes: Optional[List[str]] = Query(None), monologue_service: MonologueService = Depends(get_monologue_service)) -> List[Monologue]:
    return monologue_service.search(persona_id=persona_id, themes=themes)


@monologue_rest_router.post("/")
async def save(monologue: Monologue, monologue_service: MonologueService = Depends(get_monologue_service)):
    return monologue_service.save(monologue)

@monologue_rest_router.delete("/{monologue_id}")
async def delete(monologue_id: int, monologue_service: MonologueService = Depends(get_monologue_service)):
    return monologue_service.delete(monologue_id)