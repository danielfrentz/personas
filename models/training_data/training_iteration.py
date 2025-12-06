from pydantic import BaseModel


class TrainingIterationModel(BaseModel):
    context_length: int
    neftune_noise_alpha: float
    use_identity: bool
    use_conversation: bool

