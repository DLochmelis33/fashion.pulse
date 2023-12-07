import pytorch_lightning as pl

import argparse
import wandb
import os

from data.data_module.fashion_styles_data_module import FashionStylesDataModule
from models.fashion_style_model import FashionStylesModel
from models.lightning_model import LightningFashionStylesModel
from utils.env_utils import read_env_var

from .lightning_model_utils import setup_wandb_logger, get_model_checkpoint_callback, get_checkpoints_dir, get_wandb_dir
from .lightning_model_utils import BATCH_SIZE, NUM_CLASSES, LEARNING_RATE


def test_on_best_checkpoint(wandb_run_id: str):
    data_dir = read_env_var('DATA_DIR')
    data_module = FashionStylesDataModule(
        data_dir=data_dir, batch_size=BATCH_SIZE)

    lightning_model = LightningFashionStylesModel(
        FashionStylesModel(num_classes=NUM_CLASSES),
        learning_rate=LEARNING_RATE
    )

    wandb_logger = setup_wandb_logger(lightning_model, resume_run_id=wandb_run_id)

    run_artifact = wandb.run.use_artifact('dlhf/fashion.pulse-core_src/model-sg3yeobh:best')
    run_artifact_path = run_artifact.download(root=get_wandb_dir())
    ckpt_path = os.path.join(run_artifact_path, 'model.ckpt')

    trainer = pl.Trainer(
        accelerator='auto',
        devices='auto',
        logger=wandb_logger,
        callbacks=[get_model_checkpoint_callback()]
    )
    trainer.test(model=lightning_model, datamodule=data_module,
                 ckpt_path=ckpt_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='predict labels for an image')
    parser.add_argument('-r', '--run_id', dest='run_id', type=str, required=True, help='wandb run id to test')
    args = parser.parse_args()

    test_on_best_checkpoint(args.run_id)
    wandb.finish()
