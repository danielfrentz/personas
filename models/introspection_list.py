from typing import List

from pydantic import BaseModel

from models.introspection import Introspection


class IntrospectionList(BaseModel):
    introspections: List[Introspection]