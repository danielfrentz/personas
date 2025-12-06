from pydantic import BaseModel


class ContextParameters(BaseModel):
    starting_context: int
    maximum_context: int
    context_increase: int