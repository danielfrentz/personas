from converter.story_disagreement import StoryDisagreement
from entity.base import StoryDisagreementEntity


class StoryDisagreementConverter:
    def model_to_entity(self, model: StoryDisagreement) -> StoryDisagreementEntity:
        return StoryDisagreementEntity(
            id=model.id,
            name=model.name,
            details=model.details,
            story_id=model.story_id,
        )

    def entity_to_model(self, entity: StoryDisagreementEntity) -> StoryDisagreement:
        return StoryDisagreement(
            id=entity.id,
            name=entity.name,
            details=entity.details,
            story_id=entity.story_id,
        )