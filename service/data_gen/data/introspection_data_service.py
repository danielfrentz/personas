import logging
from typing import List

from models.conversation import Conversation
from models.persona import Persona
from service.persona_domain.introspection_service import IntrospectionService
from service.persona_domain.persona_service import PersonaService


class IntrospectionDataService:
    def __init__(self, introspection_service: IntrospectionService, persona_service: PersonaService):
        self.introspection_service = introspection_service
        self.persona_service = persona_service
        self.introspection_service = introspection_service


    def generate(self, persona_id) -> List[Conversation]:
        persona: Persona = self.persona_service.find_by_id(persona_id)
        result: List[Conversation] = []
        for life_event in persona.life_events:
            if life_event.story:
                if life_event.story:
                    introspections = self.introspection_service.find_by_story_id(story_id=life_event.story.id)
                    if introspections:
                        print(len(introspections))
                        for introspection in introspections:
                            result.append(introspection.monologue)
        logging.info(f"returning {len(result)} introspections")
        return result