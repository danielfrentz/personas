from converter.story_converter import StoryConverter
from entity.base import LifeEventEntity
from models.ai.output.life_event_ai import LifeEventAI
from models.life_event import LifeEvent
from models.story import Story

class LifeEventConverter:
    def __init__(self, story_converter: StoryConverter):
        self.story_converter = story_converter

    def model_to_entity(self, life_event_model: LifeEvent) -> LifeEventEntity:
        result = LifeEventEntity(
            id=life_event_model.id,
            title=life_event_model.title.lower(),
            description=life_event_model.description,
            date=life_event_model.date,
            detail_learned=life_event_model.detail_learned,
            persona_id=life_event_model.persona_id
        )
        return result

    def entity_to_model(self, life_event_entity: LifeEventEntity) -> LifeEvent:
        story: Story = self.story_converter.entity_to_model(life_event_entity.story)
        return LifeEvent(
            id=life_event_entity.id,
            title=life_event_entity.title.lower(),
            description=life_event_entity.description,
            date=life_event_entity.date,
            detail_learned=life_event_entity.detail_learned,
            persona_id=life_event_entity.persona_id,
            story=story
        )

    def ai_to_model(self, life_event_ai: LifeEventAI, persona_id: int) -> LifeEvent:
        return LifeEvent(
            title=life_event_ai.event_title.lower(),
            detail_learned=life_event_ai.detail_learned_about_persona,
            description=life_event_ai.description,
            date=life_event_ai.date,
            persona_id=persona_id,
        )