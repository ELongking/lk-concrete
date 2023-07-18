import torch.nn as nn


class ClsTrainProcess:
    def __init__(self, model: nn.Module):
        self.model = model


    def image_transform(self):
        pass

    def run(self):
        pass


class DetTrainProcess:
    def __init__(self):
        pass