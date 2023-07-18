import torch
import torch.nn as nn


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(3, inplanes, planes, stride=stride)
        self.bn1 = nn.BatchNorm2d(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(3, planes, planes, stride=1)
        self.bn2 = nn.BatchNorm2d(planes)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out


class ResNet(nn.Module):
    def __init__(self, layers, num_classes, width_mult=1.0):
        super(ResNet, self).__init__()

        # width calc
        self.width_mult = width_mult
        self.inplanes = int(64 * self.width_mult)

        # conv and pooling
        self.conv1 = nn.Conv2d(3, int(64 * self.width_mult), kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(int(64 * self.width_mult))
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        # res block
        self.layer1 = self._make_layer(BasicBlock, int(64 * self.width_mult), layers[0])
        self.layer2 = self._make_layer(BasicBlock, int(128 * self.width_mult), layers[1], stride=2)
        self.layer3 = self._make_layer(BasicBlock, int(256 * self.width_mult), layers[2], stride=2)
        self.layer4 = self._make_layer(BasicBlock, int(512 * self.width_mult), layers[3], stride=2)

        # avg pooling and mlp
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(int(512 * BasicBlock.expansion * self.width_mult), num_classes)

    def _make_layer(self, block, planes, blocks, stride=1):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, planes * block.expansion,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(planes * block.expansion),
            )

        layers = []
        layers.append(block(self.inplanes, planes, stride, downsample))
        self.inplanes = planes * block.expansion
        for i in range(1, blocks):
            layers.append(block(self.inplanes, planes))

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        print(x.shape)
        x = self.layer2(x)
        print(x.shape)
        x = self.layer3(x)
        print(x.shape)
        x = self.layer4(x)
        print(x.shape)

        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        print(x.shape)

        return x


def build_net(depth: int, num_classes: int) -> ResNet:
    if depth == 18:
        return ResNet(layers=[2, 2, 2, 2], num_classes=num_classes)
    elif depth == 34:
        return ResNet(layers=[3, 4, 6, 3], num_classes=num_classes)
    elif depth == 50:
        return ResNet(layers=[3, 7, 11, 5], num_classes=num_classes)
    elif depth == 101:
        return ResNet(layers=[2, 2, 22, 2], num_classes=num_classes)
    elif depth == 152:
        pass


if __name__ == '__main__':
    resnet18 = build_net(depth=18, num_classes=5)
    ipt = torch.rand(1, 3, 224, 224)
    resnet18(ipt)
