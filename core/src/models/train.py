import pytorch_lightning as pl

import wandb

from data.data_module.fashion_styles_data_module import FashionStylesDataModule
from models.fashion_style_model import FashionStylesModel
from models.lightning_model import LightningFashionStylesModel
from utils.env_utils import read_env_var

from .lightning_model_utils import setup_wandb_logger, get_model_checkpoint_callback
from .lightning_model_utils import BATCH_SIZE, LEARNING_RATE, NUM_EPOCHS, NUM_CLASSES


def train():
    data_dir = read_env_var('DATA_DIR')
    data_module = FashionStylesDataModule(
        data_dir=data_dir, batch_size=BATCH_SIZE, num_workers=2)

    model = FashionStylesModel(num_classes=NUM_CLASSES)
    lightning_model = LightningFashionStylesModel(
        model, learning_rate=LEARNING_RATE)

    wandb_logger = setup_wandb_logger(lightning_model)

    trainer = pl.Trainer(
        max_epochs=NUM_EPOCHS,
        accelerator='auto',
        devices='auto',
        logger=wandb_logger,
        log_every_n_steps=5,
        callbacks=[
            get_model_checkpoint_callback()
        ]
    )
    trainer.fit(model=lightning_model, datamodule=data_module)


if __name__ == '__main__':
    train()
    wandb.finish()
