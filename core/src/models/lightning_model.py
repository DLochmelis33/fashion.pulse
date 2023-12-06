import os
from typing import List
import torch
import torch.nn.functional as F
import pytorch_lightning as pl
import torchmetrics

from .fashion_style_model import FashionStylesModel


class LightningFashionStylesModel(pl.LightningModule):

    def _create_metrics(self, metric_names: List[str]):
        metrics = {
            'accuracy': torchmetrics.Accuracy(
                task='multiclass', 
                num_classes=self.model.num_classes,
                average='none'
            ),
            'confusion': torchmetrics.ConfusionMatrix(
                task='multiclass',
                num_classes=self.model.num_classes,
                normalize='true'
            ),
            'f1': torchmetrics.F1Score(
                task='multiclass',
                num_classes=self.model.num_classes
            )
        }
        return {name: metrics[name] for name in metric_names}

    def __init__(
            self,
            model: FashionStylesModel,
            learning_rate: float
    ):
        super().__init__()

        self.learning_rate = learning_rate
        self.model = model
        self.save_hyperparameters(ignore=['model'])

        self.train_metrics = self._create_metrics(['accuracy', 'f1'])
        self.valid_metrics = self._create_metrics(['accuracy', 'f1', 'confusion'])
        self.test_metrics = self._create_metrics(['accuracy', 'f1', 'confusion'])

    def forward(self, x):
        return self.model(x)

    def _shared_step(self, batch):
        x, y = batch
        y_pred = self(x)
        loss = F.cross_entropy(y_pred.to(torch.float), y.to(torch.float))
        return loss, y, y_pred

    def _log_train_metrics(self, y_pred, y):
        for metric_name, metric in self.train_metrics.items():
            metric.update(y_pred, y)
            self.log(f'train_{metric_name}', metric, on_epoch=True, on_step=False)
            
    def _log_val_metrics(self, y_pred, y):
        for metric_name, metric in self.val_metrics.items():
            metric.update(y_pred, y)
            self.log(f'val_{metric_name}', metric, on_epoch=True, on_step=False, prog_bar=True)
            
    def _log_test_metrics(self, y_pred, y):
        for metric_name, metric in self.test_metrics.items():
            metric.update(y_pred, y)
            self.log(f'test_{metric_name}', metric)

    def training_step(self, batch, batch_idx):
        loss, y, y_pred = self._shared_step(batch)
        self.log('train_loss', loss)
        self._log_train_metrics(y_pred, y)
        return loss

    def validation_step(self, batch, batch_idx):
        loss, y, y_pred = self._shared_step(batch)
        self.log('val_loss', loss)
        self._log_val_metrics(y_pred, y)

    def test_step(self, batch, batch_idx):
        _, true_labels, y_pred = self._shared_step(batch)
        self._log_test_metrics(y_pred, y)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        return optimizer
