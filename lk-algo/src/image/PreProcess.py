import os
import os.path as osp
import re

import numpy as np
from sklearn.utils import shuffle

from PIL import Image

import torch
from torch.utils.data import Dataset
from torchvision.transforms import *

import torch
import torch.nn as nn
import torch.nn.functional as F


class FocalLoss(nn.Module):
    def __init__(self, gamma=2, alpha=None):
        super(FocalLoss, self).__init__()
        self.gamma = gamma
        self.alpha = alpha

    def forward(self, ipt, target):
        target = F.one_hot(target, num_classes=ipt.size(-1))
        logpt = F.log_softmax(ipt, dim=-1)
        pt = torch.exp(logpt)
        focal_loss = -self.alpha * (1 - pt) ** self.gamma * logpt
        loss = torch.sum(target * focal_loss, dim=-1)
        mean_loss = torch.mean(loss)

        return mean_loss


class MixUp:
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def __call__(self, sample):
        image, label = sample
        batch_size = len(label)
        if batch_size < 2:
            return image, label

        index = torch.randperm(batch_size)
        index = index[:batch_size // 2]
        image2 = image[index]
        label2 = label[index]

        lam = np.random.beta(self.alpha, self.alpha)
        lam = max(lam, 1 - lam)

        mixed_image = lam * image + (1 - lam) * image2
        mixed_label = lam * label + (1 - lam) * label2

        return mixed_image, mixed_label


class CutMix:
    def __init__(self, alpha=0.6):
        self.alpha = alpha

    def __call__(self, sample):
        image, label = sample
        batch_size = len(label)
        if batch_size < 2:
            return image, label

        index = torch.randperm(batch_size)
        index = index[:batch_size // 2]
        image2 = image[index]
        label2 = label[index]

        lam = np.random.beta(self.alpha, self.alpha)
        lam = max(lam, 1 - lam)
        bbx1, bby1, bbx2, bby2 = self.rand_bbox(image.size(), lam)

        mixed_image = image.clone()
        mixed_image[:, :, bbx1:bbx2, bby1:bby2] = image2[:, :, bbx1:bbx2, bby1:bby2]
        mixed_label = lam * label + (1 - lam) * label2

        return mixed_image, mixed_label

    @staticmethod
    def rand_bbox(size, lam):
        W = size[2]
        H = size[1]
        cut_rat = np.sqrt(1. - lam)
        cut_w = np.int(W * cut_rat)
        cut_h = np.int(H * cut_rat)

        cx = np.random.randint(W)
        cy = np.random.randint(H)

        bbx1 = np.clip(cx - cut_w // 2, 0, W)
        bby1 = np.clip(cy - cut_h // 2, 0, H)
        bbx2 = np.clip(cx + cut_w // 2, 0, W)
        bby2 = np.clip(cy + cut_h // 2, 0, H)

        return bbx1, bby1, bbx2, bby2


class ClsDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self._read_dir()

    def __len__(self):
        pass

    def __getitem__(self, index):
        image = self.data[index]
        label = self.labels[index]
        if self.transform:
            image = self.transform(image)

        return image, label

    def _read_dir(self):
        self.data, self.labels = [], []
        combine_data = []
        txt_path = osp.join(self.data_dir, 'image', "annotation")
        f = open(txt_path, "r", encoding='utf-8')
        for line in f.readlines():
            if line:
                line = line.strip()
                info = re.split(r'\s+', line)
                img_name, classes = info[0], info[1:]
                img_path = osp.join(self.data_dir, "image", "image", img_name)
                image = Image.open(img_path)
                for label in classes:
                    combine_data.append([image, label])

        combine_data = shuffle(combine_data, random_state=42)
        for img, lab in combine_data:
            self.data.append(img)
            self.labels.append(lab)


class ImageAugMethod:
    def __init__(self):
        self.base_aug = {
            "tensor": ToTensor(),
            "mean": Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            "resize": Resize(256)
        }
        self.advanced_aug = {
            "crop": RandomCrop(224),
            "randaug": RandAugment(),
            "cutmix": CutMix(),
            "mixup": MixUp()
        }

    def get_transform_method(self, aug_params: dict) -> Compose:
        compose = [
            self.base_aug["mean"],
            self.base_aug["resize"],
        ]
        for key, val in aug_params.items():
            compose.append(self.advanced_aug[key])
            pass
