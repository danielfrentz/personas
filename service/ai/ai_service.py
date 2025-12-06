import logging

from fastapi import HTTPException

from config.settings import Settings
from models.analytics.prompt_performance import PromptPerformance
from service.analytics.prompt_performance_service import PromptPerformanceService

logger = logging.getLogger("ai_service")
from time import time
from typing import Type
import ollama
from pydantic import BaseModel


class AIService:
    def __init__(self, prompts_service,
                 model,
                 tokenizer,
                 prompt_performance_service: PromptPerformanceService,
                 settings: Settings):
        self.prompts_service = prompts_service
        self.model = model
        self.tokenizer = tokenizer
        self.prompt_performance_service = prompt_performance_service
        self.model = settings.ollama_model


    def call_ollama(self, system_prompt, user_data, response_type: Type[BaseModel]) -> str:
        try:
            client = ollama.Client(timeout=360)
            chat_response = client.generate(model=self.model,
                                            system=system_prompt + "\n" + user_data,
                                            prompt=system_prompt + "\n" + user_data,
                                            think=True,
                                            # prompt=system_prompt,
                                            format=response_type.model_json_schema())
            response = chat_response['response']
            logger.info("Raw LLM response: {}".format(response))
            return response
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Got exception {ex} when calling Ollama.")


    def call_llm(self, system_prompt_name, return_type: Type[BaseModel], user_data: BaseModel, universe_id: int=None, validator=None):
        logger.debug(f"Calling generate for prompt {system_prompt_name}")
        start_time = time()
        success = False
        result = None
        failures = 0
        system_prompt, user_prompt = self.prompts_service.get_prompt(prompt_name=system_prompt_name,
                                                                     user_data=user_data, universe_id=universe_id)
        while not success and failures < 3:
            logger.debug(f"system prompt is {system_prompt}")
            logger.debug(f"user prompt is {user_prompt}")
            raw_result = self.call_ollama(system_prompt=system_prompt,
                                          response_type=return_type,
                                          user_data=user_prompt)
            raw_result = raw_result.strip()
            raw_result = raw_result.lower()
            logger.debug(f"raw output is: {raw_result}")
            try:
                result = return_type.model_validate_json(raw_result)
                for field, value in result:
                    if value == "...":
                        raise ValueError(f"LLM returned {value} for field {field}.")
                if validator:
                    validator(result)
                total_time = time() - start_time
                logger.info(f"total time to call {system_prompt_name} was {total_time}")
                success = True
                prompt_performance_payload = PromptPerformance(
                    template_name=system_prompt_name,
                    prompt=user_prompt,
                    response=raw_result,
                    time_taken=total_time,
                    model=self.model,
                )
                self.prompt_performance_service.save(prompt_performance_payload)

            except Exception as ex:
                failures+=1
                logger.error(f"got exception {ex} on the {failures}th attempt.")
        if not success:
            raise HTTPException(status_code=500, detail=f"Failed to generate response for prompt {system_prompt_name}.")
        return result


