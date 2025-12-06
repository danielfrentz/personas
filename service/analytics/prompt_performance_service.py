from converter.prompt_performance_converter import PromptPerformanceConverter
from dao.prompt_performance_dao import PromptPerformanceDAO


class PromptPerformanceService:
    def __init__(self,
                 prompt_performance_dao: PromptPerformanceDAO,
                 prompt_performance_converter: PromptPerformanceConverter):
        self.prompt_performance_dao = prompt_performance_dao
        self.prompt_performance_converter = prompt_performance_converter

    def save(self, prompt_performance):
        prompt_performance_entity = self.prompt_performance_converter.model_to_entity(prompt_performance)
        self.prompt_performance_dao.save(prompt_performance_entity)