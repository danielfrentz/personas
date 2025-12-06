from http.client import HTTPException
from typing import List

from converter.backstory_converter import BackstoryConverter
from converter.life_event_converter import LifeEventConverter
from dao.life_event_dao import LifeEventDAO
from entity.base import LifeEventEntity
from models.ai.input.life_event_input import LifeEventInput
from models.ai.output.life_event_ai import LifeEventAI
from models.http.request.generate.life_event_request import LifeEventRequest
from models.life_event import LifeEvent
from models.persona import Persona
from service.ai.ai_service import AIService
from service.persona_domain.persona_service import PersonaService


class LifeEventService:
    def __init__(self, ai_service: AIService,
                 life_event_dao: LifeEventDAO,
                 life_event_converter: LifeEventConverter,
                 persona_service: PersonaService,
                 backstory_converter: BackstoryConverter):
        self.ai_service = ai_service
        self.life_event_dao = life_event_dao
        self.life_event_converter = life_event_converter
        self.persona_service = persona_service
        self.backstory_converter = backstory_converter

    def generate(self, persona_id: int, life_event_request: LifeEventRequest) -> LifeEvent:
        persona: Persona = self.persona_service.find_by_id(persona_id)
        life_event_input = LifeEventInput(
            backstory = persona.backstory,
            previous_life_events=[life_event.title.strip() for life_event in persona.life_events],
            provided_title=life_event_request.title,
            provided_context=life_event_request.context,
            historical=persona.historical
        )
        generated_life_events: LifeEventAI = self.ai_service.call_llm("create_life_events",
                                                                      LifeEventAI,
                                                                      life_event_input,
                                                                      persona.universe_id,
                                                                      validator=self.create_validation(life_event_input))
        generated_life_events.event_title = generated_life_events.event_title.replace("_", " ")
        return self.life_event_converter.ai_to_model(generated_life_events, persona_id=persona_id)

    def create_validation(self, life_event_input: LifeEventInput):
        def validation(life_event_ai: LifeEventAI):
            if life_event_ai.event_title in life_event_input.previous_life_events:
                raise HTTPException(f"The title {life_event_ai.event_title} is taken. Life event must be unique.")
        return validation

    def create(self, life_event: LifeEvent, persona_id: int):
        life_event_entity = self.life_event_converter.model_to_entity(life_event)
        life_event_entity.persona_id = persona_id
        life_event_entity = self.life_event_dao.save(life_event_entity)
        return self.life_event_converter.entity_to_model(life_event_entity)

    def find_by_id(self, life_event_id) -> LifeEvent:
        life_event_entity = self.life_event_dao.find_by_id(life_event_id)
        return self.life_event_converter.entity_to_model(life_event_entity)

    def find_by_persona_id(self, persona_id) -> List[LifeEvent]:
        life_event_entities: List[LifeEventEntity] = self.life_event_dao.find_by_persona_id(persona_id)
        return [self.life_event_converter.entity_to_model(life_event_entity) for life_event_entity in life_event_entities]

    def delete(self, life_event_id: int):
        self.life_event_dao.delete(life_event_id)