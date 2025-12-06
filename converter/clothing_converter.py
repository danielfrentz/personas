from entity.base import ClothingEntity
from models.ai.output.clothing_ai import ClothingAI
from models.clothing import Clothing


class ClothingConverter:
    def entity_to_model(self, clothing_entity: ClothingEntity) -> Clothing:
        result = Clothing(
            id=clothing_entity.id,
            clothing_name=clothing_entity.name,
            clothing_category=clothing_entity.clothing_category,
            description=clothing_entity.description,
            purpose=clothing_entity.purpose,
            occasion=clothing_entity.occasion,
            physical_description_id=clothing_entity.physical_description_id,
            personal_significance=clothing_entity.personal_significance,
            diffusion_model_description=clothing_entity.diffusion_model_description
        )
        return result
    def model_to_entity(self, clothing) -> ClothingEntity:
        result = ClothingEntity(
            id=clothing.id,
            description=clothing.description,
            occasion=clothing.occasion,
            purpose=clothing.purpose,
            clothing_category=clothing.clothing_category,
            physical_description_id=clothing.physical_description_id,
            name=clothing.clothing_name,
            personal_significance=clothing.personal_significance,
            diffusion_model_description=clothing.diffusion_model_description
        )
        return result

    def ai_to_model(self, model: ClothingAI, physical_description_id: int) -> Clothing:
        return Clothing(
            clothing_name=model.clothing_name,
            description=model.detailed_description,
            occasion=model.occasion,
            purpose=model.purpose,
            clothing_category=model.clothing_type,
            physical_description_id=physical_description_id,
            personal_significance=model.personal_significance,
            diffusion_model_description=model.diffusion_model_description
        )