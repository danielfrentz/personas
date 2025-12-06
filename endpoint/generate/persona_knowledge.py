from fastapi import APIRouter, Depends

from endpoint import get_persona_knowledge_service
from service.persona_domain.persona_knowledge_service import PersonaKnowledgeService

persona_knowledge_generate_router = APIRouter(prefix="/{persona_id}/knowledge")

@persona_knowledge_generate_router.post("/")
async def generate_persona_knowledge(persona_id: int, universe_id: int, persona_knowledge_service: PersonaKnowledgeService = Depends(get_persona_knowledge_service)):
    return persona_knowledge_service.generate(persona_id=persona_id, universe_id=universe_id)