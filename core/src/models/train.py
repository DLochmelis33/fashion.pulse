import pytorch_lightning as pl

import wandb

from data.data_module.fashion_styles_data_module import FashionStylesDataModule
from models.fashion_style_model import FashionStylesModel
from models.lightning_model import LightningFashionStylesModel
from utils.env_utils import read_env_var

from .lightning_model_utils import setup_wandb_logger
from .lightning_model_utils import BATCH_SIZE, LEARNING_RATE, NUM_EPOCHS


def train():
    data_dir = read_env_var('DATA_DIR')
    data_module = FashionStylesDataModule(
        data_dir=data_dir, batch_size=BATCH_SIZE)

    model = FashionStylesModel(num_classes=data_module.num_classes)
    lightning_model = LightningFashionStylesModel(
        model, learning_rate=LEARNING_RATE, class_names=data_module.dataset.classes)

    wandb_logger = setup_wandb_logger(lightning_model)

    trainer = pl.Trainer(
        max_epochs=NUM_EPOCHS,
        accelerator='auto',
        devices='auto',
        logger=wandb_logger,
        log_every_n_steps=100
    )
    trainer.fit(model=lightning_model, datamodule=data_module)


if __name__ == '__main__':
    train()
    wandb.finish()
