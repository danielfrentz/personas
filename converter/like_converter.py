from entity.base import LikesEntity
from models.ai.output.like_ai import LikeAI
from models.like import Like


class LikeConverter:
    """

    """
    def model_to_entity(self, like_model: Like) -> LikesEntity:
        return LikesEntity(
            backstory_id=like_model.backstory_id,
            like_reason=like_model.like_reason,
            dislike_name=like_model.dislike_name.lower(),
            dislike_reason=like_model.dislike_reason,
            like_name=like_model.like_name.lower(),
            contradiction=like_model.contradiction,
            contradiction_explanation=like_model.contradiction_explanation,
        )

    def entity_to_model(self, like_entity: LikesEntity) -> Like:
        return Like(
            id=like_entity.id,
            like_reason=like_entity.like_reason,
            dislike_name=like_entity.dislike_name.lower(),
            dislike_reason=like_entity.dislike_reason,
            backstory_id=like_entity.backstory_id,
            contradiction=like_entity.contradiction,
            like_name=like_entity.like_name.lower(),
            contradiction_explanation=like_entity.contradiction_explanation,
        )

    def ai_to_model(self, like_ai: LikeAI, backstory_id: int) -> Like:
        return Like(
            backstory_id=backstory_id,
            like_reason=like_ai.like_reason,
            like_name=like_ai.like_name.lower(),
            dislike_name=like_ai.dislike_name.lower(),
            dislike_reason=like_ai.dislike_reason,
            contradiction=like_ai.why_outsider_sees_as_contradiction,
            contradiction_explanation=like_ai.contradiction_explanation,
        )