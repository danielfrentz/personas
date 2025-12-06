import math
import random
from collections import deque

import numpy as np
from torch.optim.lr_scheduler import _LRScheduler

class FourierLR(_LRScheduler):
    def __init__(self, optimizer, num_training_steps, a1, a2, f1, f2, param_count, last_epoch=-1):
        self.num_training_steps = num_training_steps
        self.a1, self.a2, self.f1, self.f2 = a1, a2, f1, f2
        self.param_count = param_count
        self.count = 1
        self.avg_diff = math.inf
        self.diff_history = []
        self.loss_history = deque(maxlen=100)
        self.frequency_complete_count = 0
        self.setup_parameters()
        super().__init__(optimizer, last_epoch)

    def get_lr(self):
        result = [self.calculate_lr() for _ in self.base_lrs]
        return result

    def setup_parameters(self):
        self.count = 1
        self.a1 = self.a1
        self.a2 = self.a2
        self.f1 = self.f1
        self.f2 = self.f2
        parameters = []
        for _ in range(self.param_count):
            sub_param = {
                "a1": random.uniform(0, self.a1),
                "a2": random.uniform(0, self.a2),
                "f1": random.uniform(0, self.f1),
                "f2": random.uniform(0, self.f2),
                "phase": random.uniform(0, 2 * math.pi)
            }
            parameters.append(sub_param)
        self.parameters = parameters

    def step(self, loss=None):
        if loss is not None:
            self.loss_history.append(loss)
            if len(self.loss_history) > 1:
                diffs = [abs(self.loss_history[i] - self.loss_history[i - 1])
                         for i in range(1, len(self.loss_history))]
                avg_diff = np.mean(diffs)
                self.avg_diff = avg_diff
                self.diff_history.append(avg_diff)
        return super().step()

    def calculate_lr(self):
        if self.avg_diff < 0.1 and len(self.loss_history) > 50:
            print("setting up params")
            self.setup_parameters()
            self.frequency_complete_count += 1
            self.loss_history = []
            self.loss_history = deque(maxlen=100)
            self.count = 1

        self.count += 1
        x = self.count
        values = [(p['a1'] * math.sin(p['f1'] * x + p['phase'])) +
                  (p['a2'] * math.cos(p['f2'] * x + p['phase']))
                  for p in self.parameters]
        result = abs(
            sum(values, 0))
        result = result / (math.log(x + 1) * 100)
        return result
