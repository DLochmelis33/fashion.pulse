import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl


class FashionStylesModel(pl.LightningModule):

    def __init__(self, num_classes: int):
        super().__init__()
        self.num_classes = num_classes

        # input: (B, 3, 192, 192)
        self.conv1 = nn.Sequential(
            nn.Conv2d(
                in_channels=3,
                out_channels=32,
                kernel_size=(3, 3),
                stride=(1, 1),
                padding=1
            ),  # (B, 32, 192, 192)
            nn.BatchNorm2d(32),
            nn.ReLU()
        )
        self.pool1 = nn.Sequential(
            nn.Conv2d(
                in_channels=32,
                out_channels=32,
                kernel_size=(3, 3),
                stride=(1, 1),
                padding=1
            ),  # (B, 32, 192, 192)
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(
                kernel_size=(2, 2),
                stride=(2, 2)
            )  # (B, 32, 96, 96)
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(
                in_channels=32,
                out_channels=64,
                kernel_size=(3, 3),
                stride=(1, 1),
                padding=1
            ),  # (B, 64, 96, 96)
            nn.BatchNorm2d(64),
            nn.ReLU()
        )
        self.pool2 = nn.Sequential(
            nn.Conv2d(
                in_channels=64,
                out_channels=64,
                kernel_size=(3, 3),
                stride=(1, 1),
                padding=1
            ),  # (B, 64, 96, 96)
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(
                kernel_size=(2, 2),
                stride=(2, 2)
            )  # (B, 64, 48, 48)
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(
                in_channels=64,
                out_channels=128,
                kernel_size=(3, 3),
                stride=(1, 1),
                padding=1
            ),  # (B, 128, 48, 48)
            nn.BatchNorm2d(128),
            nn.ReLU()
        )
        self.pool3 = nn.Sequential(
            nn.Conv2d(
                in_channels=128,
                out_channels=128,
                kernel_size=(3, 3),
                stride=(1, 1),
                padding=1
            ),  # (B, 128, 48, 48)
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(
                kernel_size=(2, 2),
                stride=(2, 2)
            )  # (B, 128, 24, 24)
        )
        self.conv4 = nn.Sequential(
            nn.Conv2d(
                in_channels=128,
                out_channels=256,
                kernel_size=(3, 3),
                stride=(1, 1),
                padding=1
            ),  # (B, 256, 24, 24)
            nn.BatchNorm2d(256),
            nn.ReLU()
        )
        self.pool4 = nn.Sequential(
            nn.Conv2d(
                in_channels=256,
                out_channels=256,
                kernel_size=(3, 3),
                stride=(1, 1),
                padding=1
            ),  # (B, 256, 24, 24)
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(
                kernel_size=(2, 2),
                stride=(2, 2)
            )  # (B, 256, 12, 12)
        )
        self.conv5 = nn.Sequential(
            nn.Conv2d(
                in_channels=256,
                out_channels=512,
                kernel_size=(3, 3),
                stride=(1, 1),
                padding=1
            ),  # (B, 512, 12, 12)
            nn.BatchNorm2d(512),
            nn.ReLU()
        )
        self.pool5 = nn.Sequential(
            nn.Conv2d(
                in_channels=512,
                out_channels=512,
                kernel_size=(3, 3),
                stride=(1, 1),
                padding=1
            ),  # (B, 512, 12, 12)
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(
                kernel_size=(2, 2),
                stride=(2, 2)
            )  # (B, 512, 6, 6)
        )
        self.classifier = nn.Sequential(
            self.conv1,
            self.pool1,
            self.conv2,
            self.pool2,
            self.conv3,
            self.pool3,
            self.conv4,
            self.pool4,
            self.conv5,
            self.pool5,
            nn.Flatten(),  # (B, 512 * 6 * 6)
            nn.Dropout(0.5),
            nn.Linear(512 * 6 * 6, 2048),  # (B, 2048)
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(2048, 2048),  # (B, 2048)
            nn.ReLU(),
            nn.Linear(2048, self.num_classes),  # (B, num_classes)
            nn.Sigmoid()
        )

    def forward(self, x):
        y_pred = self.classifier(x)
        return y_pred
