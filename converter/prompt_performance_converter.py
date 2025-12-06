from entity.base import PromptPerformanceEntity
from models.analytics.prompt_performance import PromptPerformance


class PromptPerformanceConverter:

    def model_to_entity(self, prompt_performance: PromptPerformance) -> PromptPerformanceEntity:
        return PromptPerformanceEntity(
            id=prompt_performance.id,
            prompt=prompt_performance.prompt,
            response=prompt_performance.response,
            model=prompt_performance.model,
            time_taken=prompt_performance.time_taken,
            template_name=prompt_performance.template_name
        )

    def entity_to_model(self, prompt_performance_entity: PromptPerformanceEntity) -> PromptPerformance:
        return PromptPerformance(
            id=prompt_performance_entity.id,
            prompt=prompt_performance_entity.prompt,
            response=prompt_performance_entity.response,
            model=prompt_performance_entity.model,
            time_taken=prompt_performance_entity.time_taken,
            template_name=prompt_performance_entity.template_name
        )