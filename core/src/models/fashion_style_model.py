# class DlhfModel(pl.LightningModule):
#     """Simple CNN according to ChatGPT"""

#     def __init__(self, num_classes):
#         super().__init__()
#         self.num_classes = num_classes

#         # input: (B, 3, 128, 128)
#         self.block1 = nn.Sequential(
#             nn.Conv2d(
#                 in_channels=3,
#                 out_channels=32,
#                 kernel_size=(3, 3),
#                 stride=(1, 1),
#                 padding=1
#             ), # (B, 32, 128, 128)
#             nn.ReLU(),
#             nn.MaxPool2d(
#                 kernel_size=(2, 2),
#                 stride=(2, 2)
#             ) # (B, 32, 64, 64)
#         )
#         self.block2 = nn.Sequential(
#             nn.Conv2d(
#                 in_channels=32,
#                 out_channels=64,
#                 kernel_size=(3, 3),
#                 stride=(1, 1),
#                 padding=1
#             ), # (B, 64, 64, 64)
#             nn.ReLU(),
#             nn.MaxPool2d(
#                 kernel_size=(2, 2),
#                 stride=(2, 2)
#             ) # (B, 64, 32, 32)
#         )
#         self.block3 = nn.Sequential(
#             nn.Conv2d(
#                 in_channels=64,
#                 out_channels=128,
#                 kernel_size=(3, 3),
#                 stride=(1, 1),
#                 padding=1
#             ), # (B, 128, 32, 32)
#             nn.ReLU(),
#             nn.MaxPool2d(
#                 kernel_size=(2, 2),
#                 stride=(2, 2)
#             )  # (B, 128, 16, 16)
#         )
#         self.classifier = nn.Sequential(
#             self.block1,
#             self.block2,
#             self.block3,
#             nn.Flatten(), # (B, 128 * 16 * 16)
#             nn.Linear(128 * 16 * 16, 128), # (B, 128)
#             nn.ReLU(),
#             nn.Linear(128, self.num_classes), # (B, num_classes)
#             nn.Sigmoid()
#         )

#     def forward(self, x):
#         y_pred = self.classifier(x)
#         return y_pred


# class DlhfLightningModel(pl.LightningModule):

#     def _create_accuracy(self):
#         return torchmetrics.Accuracy(task='multilabel', num_labels=self.model.num_classes)

#     def __init__(self, model, learning_rate):
#         super().__init__()

#         self.learning_rate = learning_rate
#         self.model = model
#         self.save_hyperparameters(ignore=['model'])

#         self.train_acc = self._create_accuracy()
#         self.valid_acc = self._create_accuracy()
#         self.test_acc = self._create_accuracy()

#     def forward(self, x):
#         return self.model(x)

#     def _shared_step(self, batch):
#         x, y = batch
#         y_pred = self(x)
#         loss = F.binary_cross_entropy(y_pred.to(torch.float), y.to(torch.float))
#         return loss, y, y_pred

#     def training_step(self, batch, batch_idx):
#         loss, y, y_pred = self._shared_step(batch)
#         self.log("train_loss", loss)
#         self.train_acc.update(y_pred, y)
#         self.log("train_acc", self.train_acc, on_epoch=True, on_step=False)
#         return loss

#     def validation_step(self, batch, batch_idx):
#         loss, y, y_pred = self._shared_step(batch)
#         self.log("valid_loss", loss)
#         self.valid_acc(y_pred, y)
#         self.log("valid_acc", self.valid_acc,
#                  on_epoch=True, on_step=False, prog_bar=True)

#     def test_step(self, batch, batch_idx):
#         loss, true_labels, y_pred = self._shared_step(batch)
#         self.test_acc(y_pred, true_labels)
#         self.log("test_acc", self.test_acc, on_epoch=True, on_step=False)

#     def configure_optimizers(self):
#         optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
#         return optimizer