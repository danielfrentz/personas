from converter.accessory_converter import AccessoryConverter
from converter.clothing_converter import ClothingConverter
from converter.hair_style_converter import HairStyleConverter
from converter.interesting_physical_description_note_converter import InterestingPhysicalDescriptionNoteConverter
from entity.base import PhysicalDescriptionEntity
from models.ai.output.physical_description_ai import PhysicalDescriptionAI
from models.physical_description import PhysicalDescription


class PhysicalDescriptionConverter:

    def __init__(self,
                 clothing_converter: ClothingConverter,
                 accessory_converter: AccessoryConverter,
                 hairstyle_converter: HairStyleConverter,
                 interesting_notes_converter: InterestingPhysicalDescriptionNoteConverter):
        self.clothing_converter = clothing_converter
        self.accessory_converter = accessory_converter
        self.hairstyle_converter = hairstyle_converter
        self.interesting_notes_converter = interesting_notes_converter

    def model_to_entity(self, model: PhysicalDescription) -> PhysicalDescriptionEntity | None:
        if model is None:
            return None
        result = PhysicalDescriptionEntity(
            detailed_description=model.detailed_description,
            presentation=model.presentation,
            hair_color=model.hair_color,
            height=model.height,
            weight=model.weight,
            diffusion_model_description=model.diffusion_model_description
        )
        result.accessories = [self.accessory_converter.model_to_entity(accessory=accessory) for accessory in model.accessories]
        result.clothing = [self.clothing_converter.model_to_entity(clothing) for clothing in model.clothing]
        result.hair_style = [self.hairstyle_converter.model_to_entity(hairstyle=hairstyle) for hairstyle in model.hair_style]
        result.interesting_notes = [self.interesting_notes_converter.model_to_entity(note) for note in model.interesting_notes]
        return result


    def entity_to_model(self, entity: PhysicalDescriptionEntity) -> PhysicalDescription | None:
        if entity is None:
            return None
        result = PhysicalDescription(
            id=entity.id,
            detailed_description=entity.detailed_description,
            presentation=entity.presentation,
            height=entity.height,
            weight=entity.weight,
            accessories=[self.accessory_converter.entity_to_model(accessory) for accessory in entity.accessories],
            hair_style=[self.hairstyle_converter.entity_to_model(hair_style) for hair_style in entity.hair_styles],
            clothing=[self.clothing_converter.entity_to_model(clothing) for clothing in entity.clothing],
            interesting_notes=[self.interesting_notes_converter.entity_to_model(note) for note in entity.interesting_notes],
            hair_color=entity.hair_color,
            diffusion_model_description=entity.diffusion_model_description
        )
        return result

    def ai_to_model(self, generated_physical_description: PhysicalDescriptionAI) -> PhysicalDescription:
        return PhysicalDescription(
            hair_color=generated_physical_description.hair_color,
            height=generated_physical_description.height,
            weight=generated_physical_description.weight,
            presentation=generated_physical_description.presentation,
            detailed_description=generated_physical_description.detailed_description,
            diffusion_model_description=generated_physical_description.diffusion_model_description
        )

