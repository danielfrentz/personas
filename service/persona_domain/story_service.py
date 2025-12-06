from typing import List

from converter.backstory_converter import BackstoryConverter
from converter.story_converter import StoryConverter
from dao.story_dao import StoryDAO
from models.ai.input.story_enhancement_input import StoryEnhancementInput
from models.ai.input.story_input import StoryInput
from models.ai.output.story_ai import StoryAI
from models.story import Story
from service.ai.ai_service import AIService
from service.persona_domain.life_event_service import LifeEventService
from service.persona_domain.persona_service import PersonaService
from service.persona_domain.universe_description_service import UniverseDescriptionService


class StoryService:
    def __init__(self, story_dao: StoryDAO,
                 story_converter: StoryConverter,
                 ai_service: AIService,
                 persona_service: PersonaService,
                 universe_description_service: UniverseDescriptionService,
                 life_event_service: LifeEventService,
                 backstory_converter: BackstoryConverter):
        self.story_dao = story_dao
        self.story_converter = story_converter
        self.ai_service = ai_service
        self.persona_service = persona_service
        self.universe_description_service = universe_description_service
        self.life_event_service = life_event_service
        self.backstory_converter = backstory_converter

    def save(self, story: Story) -> Story:
        story_entity = self.story_converter.model_to_entity(story)
        story_entity = self.story_dao.save(story_entity)
        return self.story_converter.entity_to_model(story_entity)

    def generate(self, persona_id: int, life_event_id: int) -> Story:
        persona = self.persona_service.find_by_id(persona_id)
        backstory = persona.backstory
        universe_description = self.universe_description_service.find_by_universe_id(universe_description_id=persona.universe_id)
        life_event = self.life_event_service.find_by_id(life_event_id)
        existing_characters = [persona.backstory for persona in self.persona_service.find_by_universe(universe_description.universe_id)]
        story_input = StoryInput(
            main_character=backstory,
            universe_description=universe_description,
            life_event=life_event,
            existing_characters=existing_characters
        )

        generated_story = self.ai_service.call_llm(system_prompt_name="create_story", return_type=StoryAI, user_data=story_input, universe_id=persona.universe_id)
        return self.story_converter.ai_to_model(generated_story, life_event_id=life_event_id)

    def enhance(self, story_id: int, persona_id: int, life_event_id: int, universe_id: int) -> Story:
        story = self.find_by_id(story_id)
        main_character = self.persona_service.find_by_id(persona_id=persona_id).backstory
        universe = self.universe_description_service.find_by_universe_id(universe_description_id=universe_id)
        life_event = self.life_event_service.find_by_id(life_event_id=life_event_id)
        story_enhancement_input = StoryEnhancementInput(
            main_character=main_character,
            story=story,
            universe=universe,
            life_event=life_event
        )
        enhanced_story_ai: StoryAI = self.ai_service.call_llm("enhance_story", StoryAI, story_enhancement_input, universe_id)
        return self.story_converter.ai_to_model(enhanced_story_ai, life_event_id=life_event_id)

    def find_by_id(self, story_id) -> Story:
        story_entity = self.story_dao.find_by_id(story_id)
        return self.story_converter.entity_to_model(story_entity)

    def delete(self, story_id: int):
        self.story_dao.delete(story_id)

    def find_by_life_event(self, life_event_id) -> List[Story]:
        story_entities = self.story_dao.find_by_life_event_id(life_event_id)
        return [self.story_converter.entity_to_model(story) for story in story_entities] if story_entities else []



