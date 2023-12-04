
# # %pip install wandb
# # !wandb login

# import os
# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from torchvision.datasets import CelebA
# from torch.utils.data import DataLoader, random_split
# from torchvision import transforms
# import pytorch_lightning as pl
# import torchmetrics

# import wandb
# from pytorch_lightning.loggers import WandbLogger

# # NUM_CLASSES = 40
# # BATCH_SIZE = 256
# # NUM_EPOCHS = 5
# # LEARNING_RATE = 0.001
# # NUM_WORKERS = 0 # can be made higher

# model = DlhfModel(num_classes=NUM_CLASSES)
# lightning_model = DlhfLightningModel(model, learning_rate=LEARNING_RATE)

# wandb_logger = WandbLogger(project='fashion-celeba-test', log_model='all')
# wandb_logger.experiment.config["batch_size"] = BATCH_SIZE
# wandb_logger.watch(lightning_model, log='all')

# trainer = pl.Trainer(
#     max_epochs=NUM_EPOCHS,
#     accelerator="auto",
#     devices="auto",
#     logger=wandb_logger,
#     log_every_n_steps=100
# )

# trainer.fit(model=lightning_model, datamodule=data_module)