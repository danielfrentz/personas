from pydantic import BaseModel, Field


class MemoryAI(BaseModel):
    unique_aspect_of_specific_memory: str = Field(description="How this memory relates to an aspect different from the others.")
    memory_text: str = Field(description="The internal monologue while remembering this, it must start with something to indicate they are remembering.")
    is_core_memory: bool = Field(description="If this is a core memory or not, there should only be one of these per story.")
    feelings_stirred: str = Field(description="The feelings the person feels as they remember this, must be a single word.")
    memory_reflex: str = Field(description="An internal thought the person has just before performing an action which reminds them of this memory.")
    memory_reflex_followup: str = Field(description="A statement they make to others directly after the memory reflex thought")
    external_factors_affecting_memory: str = Field(description="Any external factors that might affect this memory.")
    why_rememeber_this_conversation: str = Field(description="Why they remember this conversation.")