from entity.base import StoryInterestingNoteEntity
from models.story_interesting_note import StoryInterestingNote


class StoryInterestingNoteConverter:
    def model_to_entity(self, model: StoryInterestingNote) -> StoryInterestingNoteEntity:
        return StoryInterestingNoteEntity(
            id=model.id,
            name=model.name,
            details=model.details,
            story_id=model.story_id,
        )

    def entity_to_model(self, entity: StoryInterestingNoteEntity) -> StoryInterestingNote:
        return StoryInterestingNote(
            id=entity.id,
            name=entity.name,
            details=entity.details,
            story_id=entity.story_id,
        )