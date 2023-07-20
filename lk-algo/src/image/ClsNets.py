import torch
import torch.nn as nn
import math
from einops import rearrange, repeat
from einops.layers.torch import Rearrange


def _make_divisible(v, divisor, min_value=None):
    if min_value is None:
        min_value = divisor
    new_v = max(min_value, int(v + divisor / 2) // divisor * divisor)
    if new_v < 0.9 * v:
        new_v += divisor
    return new_v


class SELayerOnMobileNet(nn.Module):
    def __init__(self, channel, reduction=4):
        super(SELayerOnMobileNet, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channel, _make_divisible(channel // reduction, 8)),
            nn.ReLU(inplace=True),
            nn.Linear(_make_divisible(channel // reduction, 8), channel),
            h_sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y


class SELayerOnEfficientNet(nn.Module):
    def __init__(self, inp, oup, reduction=4):
        super(SELayerOnEfficientNet, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(oup, _make_divisible(inp // reduction, 8)),
            nn.SiLU(),
            nn.Linear(_make_divisible(inp // reduction, 8), oup),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)
        y = self.fc(y).view(b, c, 1, 1)
        return x * y


def conv_3x3_bn(in_channel, out_channel, stride, act_fn):
    return nn.Sequential(
        nn.Conv2d(in_channel, out_channel, kernel_size=3, stride=stride, padding=1, bias=False),
        nn.BatchNorm2d(out_channel),
        act_fn()
    )


def conv_1x1_bn(in_channel, out_channel, act_fn):
    return nn.Sequential(
        nn.Conv2d(in_channel, out_channel, kernel_size=1, stride=1, padding=0, bias=False),
        nn.BatchNorm2d(out_channel),
        act_fn()
    )


# --------------------------------------------------------


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_channels, out_channels, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        identity = x

        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)

        x = self.conv2(x)
        x = self.bn2(x)

        identity = self.shortcut(identity)

        x += identity
        x = self.relu(x)

        return x


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, in_channels, out_channels, stride=1):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.conv3 = nn.Conv2d(out_channels, out_channels * self.expansion, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels * self.expansion)
        self.relu = nn.ReLU(inplace=True)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels * self.expansion:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels * self.expansion, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels * self.expansion)
            )

    def forward(self, x):
        identity = x

        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)

        x = self.conv3(x)
        x = self.bn3(x)

        identity = self.shortcut(identity)

        x += identity
        x = self.relu(x)

        return x


class ResNet(nn.Module):
    def __init__(self, block, layers, num_classes):
        super(ResNet, self).__init__()
        self.in_channels = 64
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
        self.layer4 = self._make_layer(block, 512, layers[3], stride=2)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)

    def _make_layer(self, block, out_channels, blocks, stride=1):
        layers = []
        layers.append(block(self.in_channels, out_channels, stride))
        self.in_channels = out_channels * block.expansion
        for i in range(1, blocks):
            layers.append(block(self.in_channels, out_channels))

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)

        return x


def build_resnet(num_classes: int, depth: int, ) -> ResNet:
    if depth == 18:
        return ResNet(block=BasicBlock, layers=[2, 2, 2, 2], num_classes=num_classes)
    elif depth == 34:
        return ResNet(block=BasicBlock, layers=[3, 4, 6, 3], num_classes=num_classes)
    elif depth == 50:
        return ResNet(block=Bottleneck, layers=[3, 4, 6, 3], num_classes=num_classes)
    elif depth == 101:
        return ResNet(block=Bottleneck, layers=[3, 4, 23, 3], num_classes=num_classes)
    elif depth == 152:
        return ResNet(block=Bottleneck, layers=[3, 8, 36, 3], num_classes=num_classes)


# ------------------------------------------------------------------------------------------------------------

"""
Re-Implemented referred to https://github.com/d-li14/mobilenetv3.pytorch
"""


class h_sigmoid(nn.Module):
    def __init__(self, inplace=True):
        super(h_sigmoid, self).__init__()
        self.relu = nn.ReLU6(inplace=inplace)

    def forward(self, x):
        return self.relu(x + 3) / 6


class h_swish(nn.Module):
    def __init__(self, inplace=True):
        super(h_swish, self).__init__()
        self.sigmoid = h_sigmoid(inplace=inplace)

    def forward(self, x):
        return x * self.sigmoid(x)


class InvertedResidual(nn.Module):
    def __init__(self, in_channel, hidden_dim, out_channel, kernel_size, stride, use_se, use_hs):
        super(InvertedResidual, self).__init__()
        assert stride in [1, 2]

        self.identity = stride == 1 and in_channel == out_channel

        if in_channel == hidden_dim:
            self.conv = nn.Sequential(
                nn.Conv2d(hidden_dim, hidden_dim, kernel_size, stride, (kernel_size - 1) // 2, groups=hidden_dim,
                          bias=False),
                nn.BatchNorm2d(hidden_dim),
                h_swish() if use_hs else nn.ReLU(inplace=True),
                SELayerOnMobileNet(hidden_dim) if use_se else nn.Identity(),
                nn.Conv2d(hidden_dim, out_channel, kernel_size=1, stride=1, padding=0, bias=False),
                nn.BatchNorm2d(out_channel),
            )
        else:
            self.conv = nn.Sequential(
                nn.Conv2d(in_channel, hidden_dim, kernel_size=1, stride=1, padding=0, bias=False),
                nn.BatchNorm2d(hidden_dim),
                h_swish() if use_hs else nn.ReLU(inplace=True),
                nn.Conv2d(hidden_dim, hidden_dim, kernel_size, stride, (kernel_size - 1) // 2, groups=hidden_dim,
                          bias=False),
                nn.BatchNorm2d(hidden_dim),
                SELayerOnMobileNet(hidden_dim) if use_se else nn.Identity(),
                nn.Conv2d(hidden_dim, out_channel, kernel_size=1, stride=1, padding=0, bias=False),
                nn.BatchNorm2d(out_channel),
            )

    def forward(self, x):
        if self.identity:
            return x + self.conv(x)
        else:
            return self.conv(x)


class MobileNetV3(nn.Module):
    def __init__(self, cfg, mode, num_classes, width_mult=1.):
        super(MobileNetV3, self).__init__()
        self.cfg = cfg
        assert mode in ['large', 'small']

        input_channel = _make_divisible(16 * width_mult, 8)
        layers = [conv_3x3_bn(3, input_channel, 2, h_swish)]
        block = InvertedResidual
        for k, t, c, use_se, use_hs, s in self.cfg:
            output_channel = _make_divisible(c * width_mult, 8)
            exp_size = _make_divisible(input_channel * t, 8)
            layers.append(block(input_channel, exp_size, output_channel, k, s, use_se, use_hs))
            input_channel = output_channel
        self.features = nn.Sequential(*layers)

        self.conv = conv_1x1_bn(input_channel, exp_size, h_swish)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        output_channel = {'large': 1280, 'small': 1024}
        output_channel = _make_divisible(output_channel[mode] * width_mult, 8) if width_mult > 1.0 else output_channel[
            mode]
        self.classifier = nn.Sequential(
            nn.Linear(exp_size, output_channel),
            h_swish(),
            nn.Dropout(0.2),
            nn.Linear(output_channel, num_classes),
        )

        self._initialize_weights()

    def forward(self, x):
        x = self.features(x)
        x = self.conv(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
                if m.bias is not None:
                    m.bias.data.zero_()
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                m.weight.data.normal_(0, 0.01)
                m.bias.data.zero_()


def build_mobilenet(num_classes: int, mode: str):
    if mode == "large":
        cfg = [
            [3, 1, 16, 0, 0, 1],
            [3, 4, 24, 0, 0, 2],
            [3, 3, 24, 0, 0, 1],
            [5, 3, 40, 1, 0, 2],
            [5, 3, 40, 1, 0, 1],
            [5, 3, 40, 1, 0, 1],
            [3, 6, 80, 0, 1, 2],
            [3, 2.5, 80, 0, 1, 1],
            [3, 2.3, 80, 0, 1, 1],
            [3, 2.3, 80, 0, 1, 1],
            [3, 6, 112, 1, 1, 1],
            [3, 6, 112, 1, 1, 1],
            [5, 6, 160, 1, 1, 2],
            [5, 6, 160, 1, 1, 1],
            [5, 6, 160, 1, 1, 1]
        ]
    elif mode == "small":
        cfg = [
            [3, 1, 16, 1, 0, 2],
            [3, 4.5, 24, 0, 0, 2],
            [3, 3.67, 24, 0, 0, 1],
            [5, 4, 40, 1, 1, 2],
            [5, 6, 40, 1, 1, 1],
            [5, 6, 40, 1, 1, 1],
            [5, 3, 48, 1, 1, 1],
            [5, 3, 48, 1, 1, 1],
            [5, 6, 96, 1, 1, 2],
            [5, 6, 96, 1, 1, 1],
            [5, 6, 96, 1, 1, 1],
        ]

    else:
        raise NotImplemented(f"There is no mode called {mode}")
    return MobileNetV3(cfg=cfg, mode=mode, num_classes=num_classes)


# ----------------------------------------------------------------

class ShuffleV2Block(nn.Module):
    def __init__(self, in_channel, out_channel, mid_channel, *, ksize, stride):
        super(ShuffleV2Block, self).__init__()
        self.stride = stride
        assert stride in [1, 2]

        self.mid_channel = mid_channel
        self.ksize = ksize
        pad = ksize // 2
        self.pad = pad
        self.in_channel = in_channel

        outputs = out_channel - in_channel

        branch_main = [
            nn.Conv2d(in_channel, mid_channel, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(mid_channel),
            nn.ReLU(inplace=True),

            nn.Conv2d(mid_channel, mid_channel, ksize, stride, pad, groups=mid_channel, bias=False),
            nn.BatchNorm2d(mid_channel),

            nn.Conv2d(mid_channel, outputs, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(outputs),
            nn.ReLU(inplace=True),
        ]
        self.branch_main = nn.Sequential(*branch_main)

        if stride == 2:
            branch_proj = [
                nn.Conv2d(in_channel, in_channel, kernel_size=ksize, stride=stride, padding=pad, groups=in_channel,
                          bias=False),
                nn.BatchNorm2d(in_channel),
                nn.Conv2d(in_channel, in_channel, kernel_size=1, stride=1, padding=0, bias=False),
                nn.BatchNorm2d(in_channel),
                nn.ReLU(inplace=True),
            ]
            self.branch_proj = nn.Sequential(*branch_proj)
        else:
            self.branch_proj = None

    def forward(self, old_x):
        if self.stride == 1:
            x_proj, x = self.channel_shuffle(old_x)
            return torch.cat((x_proj, self.branch_main(x)), 1)
        elif self.stride == 2:
            x_proj = old_x
            x = old_x
            return torch.cat((self.branch_proj(x_proj), self.branch_main(x)), 1)

    def channel_shuffle(self, x):
        batch_size, num_channels, height, width = x.data.size()
        assert (num_channels % 4 == 0)
        x = x.reshape(batch_size * num_channels // 2, 2, height * width)
        x = x.permute(1, 0, 2)
        x = x.reshape(2, -1, num_channels // 2, height, width)
        return x[0], x[1]


class ShuffleNetV2(nn.Module):
    def __init__(self, num_classes: int, mode: float, stage_out_channels: list):
        super(ShuffleNetV2, self).__init__()

        self.stage_repeats = [4, 8, 4]
        self.stage_out_channels = stage_out_channels
        self.mode = mode

        input_channel = self.stage_out_channels[1]
        self.first_conv = nn.Sequential(
            nn.Conv2d(3, input_channel, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(input_channel),
            nn.ReLU(inplace=True),
        )

        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.features = []
        for idxstage in range(len(self.stage_repeats)):
            numrepeat = self.stage_repeats[idxstage]
            output_channel = self.stage_out_channels[idxstage + 2]

            for i in range(numrepeat):
                if i == 0:
                    self.features.append(ShuffleV2Block(input_channel, output_channel,
                                                        mid_channel=output_channel // 2, ksize=3, stride=2))
                else:
                    self.features.append(ShuffleV2Block(input_channel // 2, output_channel,
                                                        mid_channel=output_channel // 2, ksize=3, stride=1))

                input_channel = output_channel

        self.features = nn.Sequential(*self.features)

        self.conv_last = nn.Sequential(
            nn.Conv2d(input_channel, self.stage_out_channels[-1], kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(self.stage_out_channels[-1]),
            nn.ReLU(inplace=True)
        )
        self.globalpool = nn.AvgPool2d(7)
        if self.mode == 2.0:
            self.dropout = nn.Dropout(0.2)
        self.classifier = nn.Sequential(nn.Linear(self.stage_out_channels[-1], num_classes, bias=False))
        self._initialize_weights()

    def forward(self, x):
        x = self.first_conv(x)
        x = self.maxpool(x)
        x = self.features(x)
        x = self.conv_last(x)

        x = self.globalpool(x)
        if self.mode == 2.0:
            x = self.dropout(x)
        x = x.contiguous().view(-1, self.stage_out_channels[-1])
        x = self.classifier(x)
        return x

    def _initialize_weights(self):
        for name, m in self.named_modules():
            if isinstance(m, nn.Conv2d):
                if 'first' in name:
                    nn.init.normal_(m.weight, 0, 0.01)
                else:
                    nn.init.normal_(m.weight, 0, 1.0 / m.weight.shape[1])
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0.0001)
                nn.init.constant_(m.running_mean, 0)
            elif isinstance(m, nn.BatchNorm1d):
                nn.init.constant_(m.weight, 1)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0.0001)
                nn.init.constant_(m.running_mean, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)


def build_shufflenet(num_classes: int, mode: float):
    if mode == 0.5:
        return ShuffleNetV2(num_classes=num_classes, mode=mode, stage_out_channels=[-1, 24, 48, 96, 192, 1024])
    elif mode == 1.0:
        return ShuffleNetV2(num_classes=num_classes, mode=mode, stage_out_channels=[-1, 24, 116, 232, 464, 1024])
    elif mode == 1.5:
        return ShuffleNetV2(num_classes=num_classes, mode=mode, stage_out_channels=[-1, 24, 176, 352, 704, 1024])
    elif mode == 2.0:
        return ShuffleNetV2(num_classes=num_classes, mode=mode, stage_out_channels=[-1, 24, 244, 488, 976, 2048])
    else:
        raise NotImplementedError(f"There is no mode called {mode}")


# ---------------------------------------------


class MBConv(nn.Module):
    def __init__(self, in_channel, out_channel, stride, expand_ratio, use_se):
        super(MBConv, self).__init__()
        assert stride in [1, 2]

        hidden_dim = round(in_channel * expand_ratio)
        self.identity = stride == 1 and in_channel == out_channel
        if use_se:
            self.conv = nn.Sequential(
                nn.Conv2d(in_channel, hidden_dim, kernel_size=1, stride=1, padding=0, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.SiLU(),
                nn.Conv2d(hidden_dim, hidden_dim, kernel_size=3, stride=stride, padding=1, groups=hidden_dim,
                          bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.SiLU(),
                SELayerOnEfficientNet(in_channel, hidden_dim),
                nn.Conv2d(hidden_dim, out_channel, kernel_size=1, stride=1, padding=0, bias=False),
                nn.BatchNorm2d(out_channel),
            )
        else:
            self.conv = nn.Sequential(
                nn.Conv2d(in_channel, hidden_dim, kernel_size=3, stride=stride, padding=1, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.SiLU(),
                nn.Conv2d(hidden_dim, out_channel, kernel_size=1, stride=1, padding=0, bias=False),
                nn.BatchNorm2d(out_channel),
            )

    def forward(self, x):
        if self.identity:
            return x + self.conv(x)
        else:
            return self.conv(x)


class EfficientNetV2(nn.Module):
    def __init__(self, cfg, num_classes: int, width_mult: float = 1.):
        super(EfficientNetV2, self).__init__()
        self.cfg = cfg

        input_channel = _make_divisible(24 * width_mult, 8)
        layers = [conv_3x3_bn(3, input_channel, 2, nn.SiLU)]
        block = MBConv
        for t, c, n, s, use_se in self.cfg:
            output_channel = _make_divisible(c * width_mult, 8)
            for i in range(n):
                layers.append(block(input_channel, output_channel, s if i == 0 else 1, t, use_se))
                input_channel = output_channel
        self.features = nn.Sequential(*layers)

        output_channel = _make_divisible(1792 * width_mult, 8) if width_mult > 1.0 else 1792
        self.conv = conv_1x1_bn(input_channel, output_channel, nn.SiLU)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Linear(output_channel, num_classes)

        self._initialize_weights()

    def forward(self, x):
        x = self.features(x)
        x = self.conv(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
                if m.bias is not None:
                    m.bias.data.zero_()
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                m.weight.data.normal_(0, 0.001)
                m.bias.data.zero_()


def build_efficientnet(num_classes: int, mode: str):
    if mode == "s":
        cfg = [
            [1, 24, 2, 1, 0],
            [4, 48, 4, 2, 0],
            [4, 64, 4, 2, 0],
            [4, 128, 6, 2, 1],
            [6, 160, 9, 1, 1],
            [6, 256, 15, 2, 1],
        ]
    elif mode == "m":
        cfg = [
            [1, 24, 3, 1, 0],
            [4, 48, 5, 2, 0],
            [4, 80, 5, 2, 0],
            [4, 160, 7, 2, 1],
            [6, 176, 14, 1, 1],
            [6, 304, 18, 2, 1],
            [6, 512, 5, 1, 1],
        ]
    elif mode == "l":
        cfg = [
            [1, 32, 4, 1, 0],
            [4, 64, 7, 2, 0],
            [4, 96, 7, 2, 0],
            [4, 192, 10, 2, 1],
            [6, 224, 19, 1, 1],
            [6, 384, 25, 2, 1],
            [6, 640, 7, 1, 1],
        ]
    elif mode == "xl":
        cfg = [
            [1, 32, 4, 1, 0],
            [4, 64, 8, 2, 0],
            [4, 96, 8, 2, 0],
            [4, 192, 16, 2, 1],
            [6, 256, 24, 1, 1],
            [6, 512, 32, 2, 1],
            [6, 640, 8, 1, 1],
        ]

    else:
        raise NotImplementedError(f"There is no mode called {mode}")

    return EfficientNetV2(cfg=cfg, num_classes=num_classes)


# ---------------------------------


def pair(t):
    return t if isinstance(t, tuple) else (t, t)


class PreNorm(nn.Module):
    def __init__(self, dim, fn):
        super().__init__()
        self.norm = nn.LayerNorm(dim)
        self.fn = fn

    def forward(self, x, **kwargs):
        return self.fn(self.norm(x), **kwargs)


class FeedForward(nn.Module):
    def __init__(self, dim, hidden_dim, dropout=0.):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, dim),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        return self.net(x)


class Attention(nn.Module):
    def __init__(self, dim, heads=8, dim_head=64, dropout=0.):
        super().__init__()
        inner_dim = dim_head * heads
        project_out = not (heads == 1 and dim_head == dim)

        self.heads = heads
        self.scale = dim_head ** -0.5

        self.attend = nn.Softmax(dim=-1)
        self.dropout = nn.Dropout(dropout)

        self.to_qkv = nn.Linear(dim, inner_dim * 3, bias=False)

        self.to_out = nn.Sequential(
            nn.Linear(inner_dim, dim),
            nn.Dropout(dropout)
        ) if project_out else nn.Identity()

    def forward(self, x):
        qkv = self.to_qkv(x).chunk(3, dim=-1)
        q, k, v = map(lambda t: rearrange(t, 'b n (h d) -> b h n d', h=self.heads), qkv)

        dots = torch.matmul(q, k.transpose(-1, -2)) * self.scale

        attn = self.attend(dots)
        attn = self.dropout(attn)

        out = torch.matmul(attn, v)
        out = rearrange(out, 'b h n d -> b n (h d)')
        return self.to_out(out)


class Transformer(nn.Module):
    def __init__(self, dim, depth, heads, dim_head, mlp_dim, dropout=0.):
        super().__init__()
        self.layers = nn.ModuleList([])
        for _ in range(depth):
            self.layers.append(nn.ModuleList([
                PreNorm(dim, Attention(dim, heads=heads, dim_head=dim_head, dropout=dropout)),
                PreNorm(dim, FeedForward(dim, mlp_dim, dropout=dropout))
            ]))

    def forward(self, x):
        for attn, ff in self.layers:
            x = attn(x) + x
            x = ff(x) + x
        return x


class ViT(nn.Module):
    def __init__(self,
                 image_size,
                 patch_size,
                 num_classes,
                 dim,
                 depth,
                 heads,
                 mlp_dim,
                 pool='cls',
                 channels=3,
                 dim_head=64,
                 dropout=0.,
                 emb_dropout=0.):
        super().__init__()
        image_height, image_width = pair(image_size)
        patch_height, patch_width = pair(patch_size)

        assert image_height % patch_height == 0 and image_width % patch_width == 0, 'Image dimensions must be divisible by the patch size.'

        num_patches = (image_height // patch_height) * (image_width // patch_width)
        patch_dim = channels * patch_height * patch_width
        assert pool in {'cls', 'mean'}, 'pool type must be either cls (cls token) or mean (mean pooling)'

        self.to_patch_embedding = nn.Sequential(
            Rearrange('b c (h p1) (w p2) -> b (h w) (p1 p2 c)', p1=patch_height, p2=patch_width),
            nn.LayerNorm(patch_dim),
            nn.Linear(patch_dim, dim),
            nn.LayerNorm(dim),
        )

        self.pos_embedding = nn.Parameter(torch.randn(1, num_patches + 1, dim))
        self.cls_token = nn.Parameter(torch.randn(1, 1, dim))
        self.dropout = nn.Dropout(emb_dropout)

        self.transformer = Transformer(dim, depth, heads, dim_head, mlp_dim, dropout)

        self.pool = pool
        self.to_latent = nn.Identity()

        self.mlp_head = nn.Sequential(
            nn.LayerNorm(dim),
            nn.Linear(dim, num_classes)
        )

    def forward(self, img):
        x = self.to_patch_embedding(img)
        b, n, _ = x.shape

        cls_tokens = repeat(self.cls_token, '1 1 d -> b 1 d', b=b)
        x = torch.cat((cls_tokens, x), dim=1)
        x += self.pos_embedding[:, :(n + 1)]
        x = self.dropout(x)

        x = self.transformer(x)

        x = x.mean(dim=1) if self.pool == 'mean' else x[:, 0]

        x = self.to_latent(x)

        x = self.mlp_head(x)
        return x


def build_vit(num_classes: int, mode: str) -> ViT:
    if mode == "tiny":
        return ViT(image_size=256,
                   patch_size=16,
                   num_classes=num_classes,
                   dim=192,
                   depth=12,
                   heads=3,
                   mlp_dim=768)
    elif mode == "small":
        return ViT(image_size=256,
                   patch_size=16,
                   num_classes=num_classes,
                   dim=384,
                   depth=12,
                   heads=6,
                   mlp_dim=1536)
    elif mode == "base":
        return ViT(image_size=256,
                   patch_size=16,
                   num_classes=num_classes,
                   dim=768,
                   depth=12,
                   heads=12,
                   mlp_dim=3072)
    elif mode == "large":
        return ViT(image_size=256,
                   patch_size=16,
                   num_classes=num_classes,
                   dim=1024,
                   depth=24,
                   heads=16,
                   mlp_dim=4096)

    else:
        raise NotImplementedError(f"There is no mode called {mode}")


if __name__ == '__main__':
    from thop import profile

    size = 256
    ipt = torch.rand(1, 3, size, size)

    for mode in [18, 34, 50, 101, 152]:
        model = build_resnet(2, mode)
        params = round(profile(model, (ipt,), verbose=False)[1] / 1000000, 3)
        print(f"ResNet{mode} --> {params}")
    print("-" * 50)
    for mode in [0.5, 1.0, 1.5, 2.0]:
        model = build_shufflenet(2, mode)
        params = round(profile(model, (ipt,), verbose=False)[1] / 1000000, 3)
        print(f"ShuffleNet{mode} --> {params}")
    print("-" * 50)
    for mode in ["s", "m", "l", "xl"]:
        model = build_efficientnet(2, mode)
        params = round(profile(model, (ipt,), verbose=False)[1] / 1000000, 3)
        print(f"EfficientNet{mode} --> {params}")
    print("-" * 50)
    for mode in ["small", "large"]:
        model = build_mobilenet(2, mode)
        params = round(profile(model, (ipt,), verbose=False)[1] / 1000000, 3)
        print(f"MobileNet{mode} --> {params}")
    print("-" * 50)
    for mode in ["tiny", "small", "base", "large"]:
        model = build_vit(2, mode)
        params = round(profile(model, (ipt,), verbose=False)[1] / 1000000, 3)
        print(f"ViT{mode} --> {params}")
    print("-" * 50)
