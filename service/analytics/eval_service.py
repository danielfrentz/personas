from json import dumps
from typing import List, Dict

import ollama
from pydantic import BaseModel, Field

sample_prompts = {
    "persona_consistency": """
    You are a model evaluator. Your task is to evaluate the consistency of the model's response with the answer.
    The model's response is {model_response}. The sample answer is {answer}.
    Note the answer does not have to be precisely the same as provided, merely the same meaning.
    The score must be from 1 to 5 where 1 is a complete failure and 5 is a complete success.
    Give your response in JSON format.
    """,
    "correct_answer":"""
    You are a model evaluator. Your task is to evaluate the correctness of the model's response with the provided answer.
    The model's response is {model_response}. The sample answer is {answer}.
    Note the answer does not have to be precisely the same as provided, merely the same meaning.
    The score must be from 1 to 5 where 1 is a complete failure and 5 is a complete success.
    Give your response in JSON format.
    """,
    "reasoning": """
    You are a model evaluator. Your task is to evaluate the reasoning of the model's response with the provided answer.
    The model's response is {model_response}. The sample answer is {answer}.
    Note the answer does not have to be precisely the same as provided, merely the same meaning.
    The score must be from 1 to 5 where 1 is a complete failure and 5 is a complete success.
    Give your response in JSON format.
    """,
    "realism":"""
    You are a model evaluator. Your task is to evaluate the realism of the model's response with the provided answer.
    In this context realism refers to how realistic the conversation sounds.
    The model's response is {model_response}. The sample answer is {answer}.
    The score must be from 1 to 5 where 1 is a complete failure and 5 is a complete success.
    Note the answer does not have to be precisely the same as provided, merely the same meaning.
    """,
    "solution_given":"""
    You are a model evaluator. Your task is to evaluate if the model gave a solution.
    The solution does not need to be correct but rather simply that it arrived at a solution.
    The model's response is {model_response}. The sample answer is {answer}.
    The score must be from 1 to 5 where 1 is a complete failure and 5 is a complete success.
    Note the answer does not have to be precisely the same as provided, merely the same meaning.
    """
}



class EvalResponseFormat(BaseModel):
    score: float = Field(ge=1, le=5)
    score_justification: str = Field(min_length=100)

class Problem(BaseModel):
    problem_statement: str
    minimum_llm_size: int
    test_objectives: List[str]
    answer: str

class EvalService:
    def __init__(self, prompts: Dict[str, str]):
        self.prompts = prompts

    def evaluate(self, problem: Problem, ollama_config, model, speaker: str):
        prompt = self.create_seed(question=problem.problem_statement, speaker=speaker)
        model_response = self.prompt_model(prompt)
        return self.get_eval_score(model_response=model_response, answer=problem.answer)

    def get_eval_score(self, model_response, answer):
        for prompt in self.prompts:
            ollama.generate(
                prompt=prompt.format(model_response=model_response, answer=answer),
                think=False,
                format=EvalResponseFormat.model_json_schema()
            )

    # def prompt_model(self, prompt, model, tokenizer):
    #     inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    #     with torch.no_grad():
    #         outputs = model.generate(
    #             **inputs,
    #             max_new_tokens=settings['max_new_tokens'],
    #             do_sample=settings['do_sample'],
    #             temperature=settings['temperature'],
    #             repetition_penalty=1.1,
    #             pad_token_id=tokenizer.eos_token_id
    #         )
    #         return tokenizer.decode(outputs[0], skip_special_tokens=True)

    def create_seed(self, question: str, speaker: str):
        seed_json = {
            "speaker": "User",
            "target": speaker,
            "emotion": "Curious",
            "action": "asking a question",
            "tone": "Curious",
            "speech": question
        }
        seed_json = {key: value for key, value in seed_json.items() if value is not None}
        seed_json = [seed_json]

        seed_text = dumps(seed_json, ensure_ascii=False)
        seed_text = seed_text.replace("[{", "[ {")
        seed_text = seed_text.replace("\":", "\" :")
        seed_text = seed_text.replace("{\"", "{ \"")
        seed_text = seed_text.replace("}\"", "} \"")
        seed_text = seed_text.replace("]}", "] }")
        seed_text = seed_text.replace("\",", "\" ,")
        seed_text = seed_text.replace("},", "} ,")
        seed_text = seed_text.replace("}]", "} ]")
        seed_text = seed_text.replace("[\"", "[ \"")
        seed_text = seed_text.replace("\"]", "\" ]")
        seed_text = seed_text[:len(seed_text) - 1] + ","
        return seed_text


eval_service = EvalService(prompts=sample_prompts)

def evaluate(problem: Problem, ollama_config, model, speaker: str):
    return eval_service.evaluate(problem=problem,
                                 ollama_config=ollama_config,
                                 model=model,
                                 speaker=speaker)