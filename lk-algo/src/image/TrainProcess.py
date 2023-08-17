import torch.nn as nn


class ClsTrainProcess:
    def __init__(self, model: nn.Module, cfg: dict) -> None:
        self.model = model
        self.cfg = cfg

    def run(self):
        pass


class DetTrainProcess:
    def __init__(self):
        pass
