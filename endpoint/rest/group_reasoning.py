from fastapi import APIRouter, Depends

from endpoint import get_group_reasoning_style_service
from models.group_reasoning_style import GroupReasoningStyle
from service.persona_domain.group_reasoning_profile_service import GroupReasoningProfileService

group_reasoning_style_rest_router = APIRouter(prefix="/{persona_id}/reasoning_style")

@group_reasoning_style_rest_router.post("/")
async def save(persona_id: int, group_reasoning_style: GroupReasoningStyle, reasoning_style_service: GroupReasoningProfileService = Depends(get_group_reasoning_style_service)) -> GroupReasoningStyle:
    return reasoning_style_service.save(group_reasoning_style=group_reasoning_style, persona_id=persona_id)

@group_reasoning_style_rest_router.delete("/{group_reasoning_style_id}/")
async def delete(group_reasoning_style_id: int, group_reasoning_style_service: GroupReasoningProfileService = Depends(get_group_reasoning_style_service)):
    return group_reasoning_style_service.delete(group_reasoning_style_id=group_reasoning_style_id)