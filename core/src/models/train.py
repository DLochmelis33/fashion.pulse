import pytorch_lightning as pl

import argparse
import wandb

from data.data_module.fashion_styles_data_module import FashionStylesDataModule
from models.fashion_style_model import FashionStylesModel
from models.lightning_model import LightningFashionStylesModel
from utils.env_utils import read_env_var

from .lightning_model_utils import setup_wandb_logger, get_model_checkpoint_callback
from .lightning_model_utils import BATCH_SIZE, LEARNING_RATE, NUM_CLASSES


def train(num_epochs: int, num_workers: int):
    data_dir = read_env_var('DATA_DIR')
    data_module = FashionStylesDataModule(
        data_dir=data_dir, batch_size=BATCH_SIZE, num_workers=num_workers)

    model = FashionStylesModel(num_classes=NUM_CLASSES)
    lightning_model = LightningFashionStylesModel(
        model, learning_rate=LEARNING_RATE)

    wandb_logger = setup_wandb_logger(lightning_model)

    trainer = pl.Trainer(
        max_epochs=num_epochs,
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
    parser = argparse.ArgumentParser(description='predict labels for an image')
    parser.add_argument('-n', dest='num_epochs', type=int, required=True, help='number of epochs')
    parser.add_argument('-w', dest='num_workers', type=int, default=2, help='number of workers')
    args = parser.parse_args()
    
    train(num_epochs=args.num_epochs, num_workers=args.num_workers)
    wandb.finish()
