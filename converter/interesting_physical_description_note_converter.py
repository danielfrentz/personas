from entity.base import PhysicalDescriptionInterestingNoteEntity
from models.interesting_physical_description_note import InterestingPhysicalDescriptionNote


class InterestingPhysicalDescriptionNoteConverter:
    def entity_to_model(self, entity: PhysicalDescriptionInterestingNoteEntity) -> InterestingPhysicalDescriptionNote | None:
        if entity is None:
            return None
        return InterestingPhysicalDescriptionNote(
            description=entity.description,
            id=entity.id
        )

    def model_to_entity(self, model: InterestingPhysicalDescriptionNote) -> PhysicalDescriptionInterestingNoteEntity | None:
        if model is None:
            return None
        return PhysicalDescriptionInterestingNoteEntity(
            description=model.description,
            id=model.id
        )