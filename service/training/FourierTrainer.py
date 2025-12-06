import logging
from transformers import Trainer
from service.training.FourierLR import FourierLR

logger = logging.getLogger(__name__)

def create_optimizer_and_scheduler(model, num_training_steps, a1, a2, f1, f2, param_count: int):
    print(f"passing in {len([p for p in model.parameters() if p.requires_grad])} parameters to optimizer")
    optimizer = optim.SGD((p for p in model.parameters() if p.requires_grad))
    logger.info(f"using {num_training_steps} as the number of steps")
    scheduler = FourierLR(optimizer, num_training_steps, a1, a2, f1, f2, param_count)

    return optimizer, scheduler

class CustomTrainer(Trainer):
    def create_optimizer_and_scheduler(self, num_training_steps):
        self.optimizer, self.lr_scheduler = create_optimizer_and_scheduler(self.model, num_training_steps, a1=1,
                                                                           a2=10.0,
                                                                           f1=1, f2=300, param_count=300)

    def training_step(self, model, inputs, num_items_in_batch=None):
        loss = super().training_step(model, inputs, num_items_in_batch)

        self.lr_scheduler.step(loss.item())

        return loss