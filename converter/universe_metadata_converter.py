from entity.base import UniverseMetadataEntity
from models.universe_metadata import UniverseMetadata


class UniverseMetadataConverter(object):
    def model_to_entity(self, model: UniverseMetadata) -> UniverseMetadataEntity:
        return UniverseMetadataEntity(
            id=model.id,
            name=model.name,
            description=model.description,
        )

    def entity_to_model(self, entity: UniverseMetadataEntity) -> UniverseMetadata:
        return UniverseMetadata(
            id=entity.id,
            universe_id=entity.universe_id,
            name=entity.name,
            description=entity.description,
        )
