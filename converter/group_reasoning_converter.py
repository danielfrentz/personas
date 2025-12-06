from entity.base import GroupReasoningStyleEntity
from models.ai.output.group_reasoning_style_ai import GroupReasoningStyleAI
from models.group_reasoning_style import GroupReasoningStyle


class GroupReasoningConverter:
    def model_to_entity(self, group_reasoning_style: GroupReasoningStyle) -> GroupReasoningStyleEntity | None:
        if group_reasoning_style is None:
            return None
        result = GroupReasoningStyleEntity(
            id=group_reasoning_style.id,
            tone=group_reasoning_style.tone,
            assumed_role=group_reasoning_style.assumed_role,
            reserved=group_reasoning_style.reserved,
            devils_advocate=group_reasoning_style.devils_advocate,
            persona_id=group_reasoning_style.persona_id,
            subtle=group_reasoning_style.subtle,
            sarcastic=group_reasoning_style.sarcastic,
            witty=group_reasoning_style.witty
        )
        result.persona_id = group_reasoning_style.persona_id
        return result


    def entity_to_model(self, group_reasoning_style_entity: GroupReasoningStyleEntity) -> GroupReasoningStyle | None:
        if group_reasoning_style_entity is None:
            return None
        return GroupReasoningStyle(
            subtle=group_reasoning_style_entity.subtle,
            id=group_reasoning_style_entity.id,
            devils_advocate=group_reasoning_style_entity.devils_advocate,
            sarcastic=group_reasoning_style_entity.sarcastic,
            assumed_role=group_reasoning_style_entity.assumed_role,
            persona_id=group_reasoning_style_entity.persona_id,
            tone=group_reasoning_style_entity.tone,
            reserved=group_reasoning_style_entity.reserved,
            witty=group_reasoning_style_entity.witty
        )

    def ai_to_model(self, group_reasoning_ai: GroupReasoningStyleAI, persona_id: int) -> GroupReasoningStyle:
        return GroupReasoningStyle(
            assumed_role=group_reasoning_ai.assumed_role,
            persona_id=persona_id,
            tone=group_reasoning_ai.tone,
            reserved=group_reasoning_ai.reserved,
            witty=group_reasoning_ai.witty,
            devils_advocate=group_reasoning_ai.devils_advocate,
            sarcastic=group_reasoning_ai.sarcastic,
            subtle=group_reasoning_ai.subtle,

        )