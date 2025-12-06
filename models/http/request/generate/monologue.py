from typing import Optional, List

from pydantic import BaseModel, Field


class MonologuePromptRequest(BaseModel):
    theme: str
    make_mistake: bool = Field(default=False)
    intent: str
    include_examples: bool = Field(default=False)
    include_counter_examples: bool = Field(default=False)
    speaker_ids: List[int]
    prompter_id: int
    prompt: Optional[str] = None
    solution: Optional[str] = None
    initial_monologue_id: Optional[int] = None
    custom_instructions: Optional[List[str]] = Field(default_factory=list)
    custom_prompt_requirements: Optional[List[str]] = Field(default_factory=list)
    disagreement: Optional[bool] = Field(default=False)
    prompt_type: Optional[str] = None
    minimum_turns: Optional[int] = 5
    trigger_word: Optional[str] = None