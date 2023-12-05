from pytorch_lightning.loggers import WandbLogger
from pytorch_lightning.callbacks import LambdaCallback, ModelCheckpoint

import os
import wandb

from utils.env_utils import read_env_var
from models.fashion_style_model import FashionStylesModel
from models.lightning_model import LightningFashionStylesModel

NUM_EPOCHS = 1
BATCH_SIZE = 64
LEARNING_RATE = 1e-3
NUM_CLASSES = 20

# IMPORTANT NOTE: login to wandb before training the model
# > !wandb login


def setup_wandb_logger(lightning_model: LightningFashionStylesModel, resume_run_id: str = None) -> WandbLogger:
    artifacts_dir = read_env_var('ARTIFACTS_DIR')
    wandb_dir = os.path.join(artifacts_dir, 'wandb')
    os.makedirs(wandb_dir, exist_ok=True)
    if resume_run_id is None:
        wandb.init(dir=wandb_dir)
    else:
        wandb.init(dir=wandb_dir, id=resume_run_id, resume='must')

    wandb_logger = WandbLogger(project='fashion-pulse', log_model='all')
    wandb_logger.experiment.config['batch_size'] = BATCH_SIZE
    wandb_logger.experiment.config['learning_rate'] = LEARNING_RATE
    wandb_logger.watch(lightning_model, log='all')
    return wandb_logger


def get_model_checkpoint_callback() -> ModelCheckpoint:
    checkpoints_dir = os.path.join(
        read_env_var('ARTIFACTS_DIR'), 'checkpoints')
    return ModelCheckpoint(
        monitor='valid_acc',
        mode='max',
        dirpath=checkpoints_dir
    )


def load_from_checkpoint(checkpoint_path: str) -> LightningFashionStylesModel:
    return LightningFashionStylesModel.load_from_checkpoint(
        checkpoint_path, model=FashionStylesModel(num_classes=NUM_CLASSES)
    )
