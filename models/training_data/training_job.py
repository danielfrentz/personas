from typing import List

from pydantic import BaseModel

from models.training_data.context_parameters import ContextParameters
from models.training_data.training_iteration import TrainingIterationModel


class TrainingJob(BaseModel):
    context_parameters: ContextParameters
    personas: List[str]
    iterations: List[TrainingIterationModel]
