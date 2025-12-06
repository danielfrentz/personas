from converter.persona_converter import PersonaConverter
from converter.universe_description_converter import UniverseDescriptionConverter
from converter.universe_location_converter import UniverseLocationConverter
from converter.universe_metadata_converter import UniverseMetadataConverter
from entity.base import UniverseEntity
from models.ai.output.universe_ai import UniverseDescriptionAI
from models.universe import Universe
from models.universe_description import UniverseDescription


class UniverseConverter:
    def __init__(self,
                 key_location_converter: UniverseLocationConverter,
                 universe_metadata_converter: UniverseMetadataConverter,
                 universe_description_converter: UniverseDescriptionConverter,
                 persona_converter: PersonaConverter,
                 universe_location_converter: UniverseLocationConverter,):
        self.key_location_converter = key_location_converter
        self.universe_metadata_converter = universe_metadata_converter
        self.persona_converter = persona_converter
        self.universe_description_converter = universe_description_converter
        self.persona_converter = persona_converter
        self.universe_location_converter = universe_location_converter

    def model_to_entity(self, model: Universe):
        personas = [self.persona_converter.model_to_entity(persona) for persona in model.personas]
        description = self.universe_description_converter.model_to_entity(model.description)
        universe = UniverseEntity(
            name=model.name,
        )
        universe.personas = personas
        universe.universe_description = description
        universe.universe_metadata = [self.universe_metadata_converter.model_to_entity(metadata) for metadata in model.metadata]
        return universe

    def entity_to_model(self, universe_entity: UniverseEntity) -> Universe:
        metadata = [self.universe_metadata_converter.entity_to_model(metadata) for metadata in universe_entity.universe_metadata]
        personas = [self.persona_converter.entity_to_model(entity) for entity in universe_entity.personas]
        locations = [self.universe_location_converter.entity_to_model(entity) for entity in universe_entity.locations]
        description: UniverseDescription = self.universe_description_converter.entity_to_model(universe_entity.universe_description)
        return Universe(
            description=description,
            locations=locations,
            metadata=metadata,
            personas=personas,
            id=universe_entity.id,
            name=universe_entity.name,
        )

    def ai_to_model(self, generated_description: UniverseDescriptionAI) -> UniverseDescription:
        return UniverseDescription(
            description=generated_description.updated_environment_description,
            creatures=generated_description.updated_inhabitants_description
        )