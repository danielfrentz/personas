from pydantic import BaseModel


class PersonaKnowledgeAI(BaseModel):
    knowledge_name: str
    knowledge_description: str
    knowledge_type: str
    knowledge_source: str