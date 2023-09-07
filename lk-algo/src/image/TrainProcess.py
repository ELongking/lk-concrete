import torch.nn as nn
from torch.utils.data import DataLoader

from src.image.PreProcess import ImageAugMethod, ClsDataset, OptimizerMethod, LossMethod
from src.image.Utils import AvgMeter
from src.tabular.LogText import LoggerHandler


class ClsTrainProcess:
    def __init__(self, model: nn.Module, cfg: dict, case_path: str, logger: LoggerHandler) -> None:
        self.model = model
        self.cfg = cfg
        self.case_path = case_path
        self.logger = logger

    def run(self):
        print(self.cfg)

        transform = ImageAugMethod().get_transform_method(self.cfg["aug"])
        dataset = ClsDataset(data_dir=self.case_path, transform=transform)
        dataloader = DataLoader(dataset=dataset, batch_size=self.cfg["batch_size"], shuffle=True)

        loss_meter = AvgMeter()
        optimizer = OptimizerMethod().get_optimizer(self.cfg["optimizer"])
        loss_func = LossMethod().get_loss(self.cfg["loss"])
        epoch = int(self.cfg["epoch"])

        for e in range(1, epoch + 1):
            for imgs, labels in dataloader:
                optimizer.zero_grad()
                outputs = self.model(imgs)
                loss = loss_func(outputs, labels)
                loss.backward()
                optimizer.step()
                loss_meter.update(loss.item(), imgs.size(0))

            txt = 'Batch [{}/{}], Loss: {:.4f}, Average Loss: {:.4f}'.format(e, epoch, loss.item(), loss_meter.avg)
            self.logger.tab_browser_emit(text=txt, step=2, level=1)


class DetTrainProcess:
    def __init__(self):
        pass
