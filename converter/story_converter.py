from converter.introspection_converter import IntrospectionConverter
from converter.memory_converter import MemoryConverter
from converter.story_disagreement_converter import StoryDisagreementConverter
from converter.story_interesting_note_converter import StoryInterestingNoteConverter
from entity.base import StoryEntity
from models.ai.output.story_ai import StoryAI
from models.story import Story


class StoryConverter(object):
    def __init__(self, story_disagreement_converter: StoryDisagreementConverter,
                 story_interesting_note_converter: StoryInterestingNoteConverter,
                 memory_converter: MemoryConverter,
                 introspection_converter: IntrospectionConverter,):
        self.story_disagreement_converter = story_disagreement_converter
        self.story_interesting_note_converter = story_interesting_note_converter
        self.memory_converter = memory_converter
        self.introspection_converter = introspection_converter

    def model_to_entity(self, story: Story) -> StoryEntity:
        memories = [self.memory_converter.model_to_entity(memory) for  memory in story.memories]
        result = StoryEntity(
            title=story.title,
            lead_up=story.lead_up,
            story=story.story,
            outcome=story.outcome,
            life_event_id=story.life_event_id,
        )
        result.memories = memories
        result.interesting_notes = [self.story_interesting_note_converter.model_to_entity(note) for note in story.interesting_notes]
        result.disagreements = [self.story_disagreement_converter.model_to_entity(disagreement) for disagreement in story.disagreements]
        return result

    def entity_to_model(self, story_entity: StoryEntity) -> Story | None:
        if story_entity is None:
            return None
        memories = [self.memory_converter.entity_to_model(memory) for memory in story_entity.memories] if story_entity.memories else []
        introspections = [self.introspection_converter.entity_to_model(introspection) for introspection in story_entity.introspections]
        return Story(
            title=story_entity.title,
            lead_up=story_entity.lead_up,
            story=story_entity.story,
            id=story_entity.id,
            outcome=story_entity.outcome,
            life_event_id=story_entity.life_event_id,
            disagreements=[self.story_disagreement_converter.entity_to_model(entity) for entity in story_entity.disagreements],
            interesting_notes=[self.story_interesting_note_converter.entity_to_model(interesting_note) for interesting_note in story_entity.interesting_notes],
            memories=memories,
            introspections=introspections
        )

    def ai_to_model(self, model: StoryAI, life_event_id: int) -> Story:
        return Story(

            lead_up=model.lead_up,
            title=model.story_title,
            story=model.story,
            outcome=model.outcome,
            characters=model.characters,
            life_event_id=life_event_id,
        )