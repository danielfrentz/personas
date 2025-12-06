from pydantic import BaseModel


class PersonaFactAI(BaseModel):
    fact_name: str
    how_does_this_fact_differ_from_existing_facts: str
    fact_explanation: str