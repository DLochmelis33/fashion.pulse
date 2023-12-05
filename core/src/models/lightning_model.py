import os
from typing import List
import torch
import torch.nn.functional as F
import pytorch_lightning as pl
import torchmetrics

from .fashion_style_model import FashionStylesModel


class LightningFashionStylesModel(pl.LightningModule):

    def _create_accuracy(self):
        return torchmetrics.Accuracy(task='multilabel', num_labels=self.model.num_classes)

    def __init__(
            self,
            model: FashionStylesModel,
            learning_rate: float,
            class_names: List[str] = None
    ):
        super().__init__()

        self.learning_rate = learning_rate
        self.class_names = class_names
        self.model = model
        self.save_hyperparameters(ignore=['model'])

        self.train_acc = self._create_accuracy()
        self.valid_acc = self._create_accuracy()
        self.test_acc = self._create_accuracy()

    def forward(self, x):
        return self.model(x)

    def _shared_step(self, batch):
        x, y = batch
        y_pred = self(x)
        loss = F.binary_cross_entropy(
            y_pred.to(torch.float), y.to(torch.float))
        return loss, y, y_pred

    def training_step(self, batch, batch_idx):
        loss, y, y_pred = self._shared_step(batch)
        self.log('train_loss', loss)
        self.train_acc.update(y_pred, y)
        self.log('train_acc', self.train_acc, on_epoch=True, on_step=False)
        return loss

    def validation_step(self, batch, batch_idx):
        loss, y, y_pred = self._shared_step(batch)
        self.log('valid_loss', loss)
        self.valid_acc(y_pred, y)
        self.log('valid_acc', self.valid_acc,
                 on_epoch=True, on_step=False, prog_bar=True)

    def test_step(self, batch, batch_idx):
        _, true_labels, y_pred = self._shared_step(batch)
        self.test_acc(y_pred, true_labels)
        self.log('test_acc', self.test_acc, on_epoch=True, on_step=False)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        return optimizer