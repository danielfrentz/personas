from fastapi import APIRouter, Depends

from endpoint import get_group_reasoning_style_service
from models.group_reasoning_style import GroupReasoningStyle
from service.persona_domain.group_reasoning_profile_service import GroupReasoningProfileService

group_reasoning_style_generate_router = APIRouter(prefix="/{persona_id}/reasoning_style")

@group_reasoning_style_generate_router.post("/")
async def generate(persona_id: int, universe_id: int, group_reasoning_style_service: GroupReasoningProfileService = Depends(get_group_reasoning_style_service)) -> GroupReasoningStyle:
    return group_reasoning_style_service.generate(universe_id=universe_id, persona_id=persona_id)