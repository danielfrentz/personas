from typing import List

from converter.universe_metadata_converter import UniverseMetadataConverter
from dao.universe_metadata_dao import UniverseMetadataDAO
from models.universe_metadata import UniverseMetadata


class UniverseMetadataService:
    def __init__(self,
                 universe_metadata_dao: UniverseMetadataDAO,
                 metadata_converter: UniverseMetadataConverter):
        self.universe_metadata_dao = universe_metadata_dao
        self.metadata_converter = metadata_converter

    def find_by_universe_id(self, universe_id: int) -> List[UniverseMetadata]:
        metadata_entities = self.universe_metadata_dao.find_by_universe_id(universe_id=universe_id)
        return [self.metadata_converter.entity_to_model(meta) for meta in metadata_entities]

    def delete(self, universe_metadata_id: int):
        self.universe_metadata_dao.delete(universe_metadata_id)