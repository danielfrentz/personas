from pydantic import BaseModel


class IntrospectionRequest(BaseModel):
    aspect_id: int